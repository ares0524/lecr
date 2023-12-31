import gc
from typing import Dict

import numpy as np
import torch
import torch.nn.functional as F
from sklearn.metrics import roc_auc_score, accuracy_score, f1_score
from torchvision.ops import sigmoid_focal_loss
from transformers import Trainer
from transformers.trainer_pt_utils import nested_detach

from model import Model
from samplers import ProportionalTwoClassesBatchSampler, ProportionalTwoClassesBatchSamplerDDP

from typing import Iterable, Dict
import torch.nn.functional as F
from torch import nn, Tensor
from enum import Enum


class SiameseDistanceMetric(Enum):
    """
    The metric for the contrastive loss
    """

    EUCLIDEAN = lambda x, y: F.pairwise_distance(x, y, p=2)
    MANHATTAN = lambda x, y: F.pairwise_distance(x, y, p=1)
    COSINE_DISTANCE = lambda x, y: 1 - F.cosine_similarity(x, y)


class OnlineContrastiveLoss(nn.Module):
    """
    Online Contrastive loss. Similar to ConstrativeLoss, but it selects hard positive (positives that are far apart)
    and hard negative pairs (negatives that are close) and computes the loss only for these pairs. Often yields
    better performances than  ConstrativeLoss.

    :param distance_metric: Function that returns a distance between two emeddings. The class SiameseDistanceMetric contains pre-defined metrices that can be used
    :param margin: Negative samples (label == 0) should have a distance of at least the margin value.
    :param size_average: Average by the size of the mini-batch.
    """

    def __init__(
        self, distance_metric=SiameseDistanceMetric.COSINE_DISTANCE, margin: float = 0.5
    ):
        super(OnlineContrastiveLoss, self).__init__()
        self.margin = margin
        self.distance_metric = distance_metric

    def forward(self, embeddings, labels, size_average=False):
        distance_matrix = self.distance_metric(embeddings[0], embeddings[1])
        negs = distance_matrix[labels == 0]
        poss = distance_matrix[labels == 1]

        # select hard positive and hard negative pairs
        negative_pairs = negs[negs < (poss.max() if len(poss) > 1 else negs.mean())]
        positive_pairs = poss[poss > (negs.min() if len(negs) > 1 else poss.mean())]

        positive_loss = positive_pairs.pow(2).sum()
        negative_loss = F.relu(self.margin - negative_pairs).pow(2).sum()
        loss = positive_loss + negative_loss
        return loss


class CustomTrainer(Trainer):
    def __init__(self, pos_neg_ratio=1, **kwargs):
        super().__init__(**kwargs)
        self.pos_neg_ratio = pos_neg_ratio

    def _get_train_sampler(self):
        # check if using distributed training
        pos_bsize = self.args.train_batch_size // (self.pos_neg_ratio + 1)
        if self.args.local_rank != -1:
            return ProportionalTwoClassesBatchSamplerDDP(
                np.array(self.train_dataset.labels),
                self.args.train_batch_size,
                minority_size_in_batch=pos_bsize,
                world_size=self.args.world_size,
                local_rank=self.args.local_rank,
            )

        return ProportionalTwoClassesBatchSampler(
            np.array(self.train_dataset.labels),
            self.args.train_batch_size,
            minority_size_in_batch=pos_bsize,
        )

    def compute_loss(self, model: Model, inputs: Dict, return_outputs=False):
        try:
            device = f"cuda:{model.module.local_rank}" if torch.cuda.is_available() else "cpu"
        except:
            local_rank = 0 if model.local_rank == -1 else model.local_rank
            device = f"cuda:{local_rank}" if torch.cuda.is_available() else "cpu"
        for k, v in inputs["topic_inputs"].items():
            inputs["topic_inputs"][k] = inputs["topic_inputs"][k].to(device)
        for k, v in inputs["content_inputs"].items():
            inputs["content_inputs"][k] = inputs["content_inputs"][k].to(device)
        for k, v in inputs["combined_inputs"].items():
            inputs["combined_inputs"][k] = inputs["combined_inputs"][k].to(device)
        outputs = model(
            inputs["topic_inputs"], inputs["content_inputs"], inputs["combined_inputs"]
        )

        labels = inputs.get("labels")
        try:
            model.objective = model.objective
        except:
            model.objective = model.module.objective

        if model.objective == "classification":
            # loss_fct = sigmoid_focal_loss
            loss_fct = F.binary_cross_entropy_with_logits
            loss = loss_fct(outputs.view(-1), labels.float())
        elif model.objective == "siamese":
            loss_fct = OnlineContrastiveLoss()
            loss = loss_fct(outputs, labels.float())
        elif model.objective == "both":
            loss = F.binary_cross_entropy_with_logits(
                outputs[0].view(-1), labels.float()
            ) + OnlineContrastiveLoss()(outputs[1], labels.float())
        else:
            raise ValueError("objective should be classification/siamese/both")

        if return_outputs:
            return (loss, outputs)
        return loss

    def create_optimizer(self):
        model = self.model
        no_decay = []
        for n, m in model.named_modules():
            if isinstance(
                m,
                (
                    torch.nn.BatchNorm1d,
                    torch.nn.BatchNorm2d,
                    torch.nn.LayerNorm,
                    torch.nn.LayerNorm,
                    torch.nn.GroupNorm,
                ),
            ):
                no_decay.append(n)

        optimizer_grouped_parameters = [
            {
                "params": [
                    p
                    for n, p in model.named_parameters()
                    if not any(nd in n for nd in no_decay)
                ],
                "weight_decay": self.args.weight_decay,
            },
            {
                "params": [
                    p
                    for n, p in model.named_parameters()
                    if any(nd in n for nd in no_decay)
                ],
                "weight_decay": 0.0,
            },
        ]
        optimizer_cls, optimizer_kwargs = Trainer.get_optimizer_cls_and_kwargs(
            self.args
        )
        self.optimizer = optimizer_cls(optimizer_grouped_parameters, **optimizer_kwargs)
        return self.optimizer

    def prediction_step(
        self, model, inputs, prediction_loss_only=False, ignore_keys=None
    ):
        inputs = self._prepare_inputs(inputs)
        with torch.no_grad():
            with self.compute_loss_context_manager():
                loss, outputs = self.compute_loss(model, inputs, return_outputs=True)
                loss = loss.mean().detach()

        if prediction_loss_only:
            return (loss, None, None)

        if type(outputs) == tuple:
            outputs = outputs[0]  # return only classification outputs
        outputs = outputs.float()
        outputs = nested_detach(outputs)
        del inputs["topic_inputs"]
        del inputs["content_inputs"]
        del inputs["combined_inputs"]

        gc.collect()
        return loss, outputs, inputs["labels"]


def compute_metrics(eval_preds):
    try:
        predictions = torch.sigmoid(torch.from_numpy(eval_preds.predictions)).numpy()
        auc = roc_auc_score(eval_preds.label_ids, predictions)
        accuracy = accuracy_score(eval_preds.label_ids, predictions > 0.5)
        f1 = f1_score(eval_preds.label_ids, predictions > 0.5)
        return {"AUC": auc, "acc": accuracy, "f1": f1}
    except:
        return {"f1": 0}
