# Training

### Sentence transformers

1.1 Train with margin = 0.5, sampler 1:1
1.2 Finetune with margin = 0.5, no sampler
2.1 Finetune with margin = 0.2, sampler 1:1
2.2 Finetune with margin = 0.2, no sampler

LECR sampler 1:1, gradient accumulation = 4, lr = 2e-5, margin = 0.2 => tăng 3% so với mặc định


### Models
https://huggingface.co/sentence-transformers/all-roberta-large-v1
https://huggingface.co/sentence-transformers/sentence-t5-large
https://huggingface.co/sentence-transformers/xlm-r-large-en-ko-nli-ststb/tree/main

sentence-transformers/xlm-r-large-en-ko-nli-ststb at main

#### sentence-transformers/all-MiniLM-L6-v2
NEPTUNE:
```
export NEPTUNE_PROJECT="thanhhau097/lecr"
export NEPTUNE_API_TOKEN="eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiJlMTRjM2ExOC1lYTA5LTQwODctODMxNi1jZjEzMjdlMjkxYTgifQ=="
```


Both:
```
CUDA_VISIBLE_DEVICES=0 python train.py --output_dir ./outputs/ --evaluation_strategy epoch --save_strategy epoch --save_total_limit 5 --logging_strategy steps --logging_steps 20 --fp16 --warmup_ratio 0.01 --lr_scheduler_type cosine --adam_eps 1e-6 --optim adamw_torch --do_train --do_eval --metric_for_best_model eval_loss --tokenizer_name sentence-transformers/all-MiniLM-L6-v2  --model_name sentence-transformers/all-MiniLM-L6-v2 --fold 0 --dataloader_num_workers 12 --learning_rate 8e-5  --num_train_epochs 20 --per_device_train_batch_size 160 --per_device_eval_batch_size 160 --remove_unused_columns False --overwrite_output_dir --load_best_model_at_end --objective both --max_len 256 --is_sentence_transformers
```

Classification:
```
CUDA_VISIBLE_DEVICES=1 python train.py --output_dir ./outputs_cls/ --evaluation_strategy epoch --save_strategy epoch --save_total_limit 5 --logging_strategy steps --logging_steps 20 --fp16 --warmup_ratio 0.01 --lr_scheduler_type cosine --adam_eps 1e-6 --optim adamw_torch --do_train --do_eval --metric_for_best_model eval_loss --tokenizer_name sentence-transformers/all-MiniLM-L6-v2  --model_name sentence-transformers/all-MiniLM-L6-v2 --fold 0 --dataloader_num_workers 12 --learning_rate 8e-5  --num_train_epochs 20 --per_device_train_batch_size 384 --per_device_eval_batch_size 384 --remove_unused_columns False --overwrite_output_dir --load_best_model_at_end --objective classification --max_len 256 --is_sentence_transformers --data_path ./data/supervised_correlations_generated.csv --report_to none --resume /home/thanh/shared_disk/thanh/lecr/data/siamese_model_0.82832.pth
```

Embedding: 
```
CUDA_VISIBLE_DEVICES=0 python train.py --output_dir ./outputs/ --evaluation_strategy epoch --save_strategy epoch --save_total_limit 5 --logging_strategy steps --logging_steps 20 --fp16 --warmup_ratio 0.01 --lr_scheduler_type cosine --adam_eps 1e-6 --optim adamw_torch --do_train --do_eval --metric_for_best_model eval_loss --tokenizer_name sentence-transformers/all-MiniLM-L6-v2  --model_name sentence-transformers/all-MiniLM-L6-v2 --fold 0 --dataloader_num_workers 12 --learning_rate 8e-5  --num_train_epochs 20 --per_device_train_batch_size 512 --per_device_eval_batch_size 512 --remove_unused_columns False --overwrite_output_dir --load_best_model_at_end --objective siamese --max_len 128 --is_sentence_transformers --top_k_neighbors 50
```

Translated Embedding:
```
CUDA_VISIBLE_DEVICES=0 python train.py --output_dir ./outputs_translated/ --evaluation_strategy epoch --save_strategy epoch --save_total_limit 5 --logging_strategy steps --logging_steps 200 --fp16 --warmup_ratio 0.01 --lr_scheduler_type cosine --adam_eps 1e-6 --optim adamw_torch --do_train --do_eval --metric_for_best_model eval_loss --tokenizer_name sentence-transformers/all-MiniLM-L6-v2  --model_name sentence-transformers/all-MiniLM-L6-v2 --fold 0 --dataloader_num_workers 10 --learning_rate 4e-5  --num_train_epochs 50 --per_device_train_batch_size 384 --per_device_eval_batch_size 384 --remove_unused_columns False --load_best_model_at_end --objective siamese --max_len 128 --is_sentence_transformers --top_k_neighbors 50 --resume /home/jovyan/lecr/data/siamese_model_0.8095.pth --use_translated
```

#### sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```
CUDA_VISIBLE_DEVICES=0 python train.py --output_dir ./outputs_siamese/ --evaluation_strategy epoch --save_strategy epoch --save_total_limit 5 --logging_strategy steps --logging_steps 200 --fp16 --warmup_ratio 0.1 --lr_scheduler_type cosine --adam_eps 1e-6 --optim adamw_torch --do_train --do_eval --metric_for_best_model eval_loss --tokenizer_name sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 --model_name sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 --fold 0 --dataloader_num_workers 12 --learning_rate 8e-5  --num_train_epochs 20 --per_device_train_batch_size 128 --per_device_eval_batch_size 128 --remove_unused_columns False --overwrite_output_dir --load_best_model_at_end --objective siamese --max_len 128 --is_sentence_transformers --top_k_neighbors 50
```

#### sentence-transformers/all-mpnet-base-v2 
CUDA_VISIBLE_DEVICES=0 python train.py --output_dir ./outputs_all-mpnet-base-v2/ --evaluation_strategy epoch --save_strategy epoch --save_total_limit 5 --logging_strategy steps --logging_steps 200 --fp16 --warmup_ratio 0.1 --lr_scheduler_type cosine --adam_eps 1e-6 --optim adamw_torch --do_train --do_eval --metric_for_best_model eval_loss --tokenizer_name sentence-transformers/all-mpnet-base-v2  --model_name sentence-transformers/all-mpnet-base-v2 --fold 0 --dataloader_num_workers 32 --learning_rate 2e-5  --num_train_epochs 50 --per_device_train_batch_size 128 --per_device_eval_batch_size 128 --remove_unused_columns False --load_best_model_at_end --objective siamese --max_len 128 --top_k_neighbors 50

### xlm-roberta-base
```
CUDA_VISIBLE_DEVICES=0 python train.py --output_dir ./outputs/ --evaluation_strategy epoch --save_strategy epoch --save_total_limit 5 --logging_strategy steps --logging_steps 200 --fp16 --warmup_ratio 0.1 --lr_scheduler_type cosine --adam_eps 1e-6 --optim adamw_torch --do_train --do_eval --metric_for_best_model eval_loss --tokenizer_name xlm-roberta-base  --model_name xlm-roberta-base --fold 0 --dataloader_num_workers 32 --learning_rate 2e-5 --num_train_epochs 50 --per_device_train_batch_size 128 --per_device_eval_batch_size 128 --remove_unused_columns False --load_best_model_at_end --objective siamese --max_len 128 --top_k_neighbors 50
```
# LLaMA 

This repository is intended as a minimal, hackable and readable example to load [LLaMA](https://ai.facebook.com/blog/large-language-model-llama-meta-ai/) ([arXiv](https://arxiv.org/abs/2302.13971v1)) models and run inference.
In order to download the checkpoints and tokenizer, fill this [google form](https://forms.gle/jk851eBVbX1m5TAv5) or if you want to save our bandwidth use this BitTorrent link: "[magnet:?xt=urn:btih:ZXXDAUWYLRUXXBHUYEMS6Q5CE5WA3LVA&dn=LLaMA](magnet:?xt=urn:btih:ZXXDAUWYLRUXXBHUYEMS6Q5CE5WA3LVA&dn=LLaMA)".

### Setup
In a conda env with pytorch / cuda available, run
### e5-small

```
python -m torch.distributed.launch --nproc_per_node 2 train.py --output_dir ./outputs_e5_small/ --evaluation_strategy epoch --save_strategy epoch --save_total_limit 2 --logging_strategy steps --logging_steps 50 --fp16 --warmup_ratio 0.01 --lr_scheduler_type cosine --adam_eps 1e-6 --optim adamw_torch --do_train --do_eval --metric_for_best_model eval_loss --tokenizer_name intfloat/e5-small --model_name intfloat/e5-small --fold 0 --dataloader_num_workers 48 --learning_rate 8e-5 --num_train_epochs 40 --per_device_train_batch_size 256 --per_device_eval_batch_size 256 --remove_unused_columns False --overwrite_output_dir --load_best_model_at_end --objective siamese --max_len 128 --is_sentence_transformers --top_k_neighbors 50 --report_to --gradient_accumulation_steps 4 none
```
### sentence-transformers/paraphrase-MiniLM-L3-v2
```
python -m torch.distributed.launch --nproc_per_node 2 train.py --output_dir ./outputs_e5_small/ --evaluation_strategy epoch --save_strategy epoch --save_total_limit 2 --logging_strategy steps --logging_steps 50 --fp16 --warmup_ratio 0.01 --lr_scheduler_type cosine --adam_eps 1e-6 --optim adamw_torch --do_train --do_eval --metric_for_best_model eval_loss --tokenizer_name sentence-transformers/paraphrase-MiniLM-L3-v2 --model_name sentence-transformers/paraphrase-MiniLM-L3-v2 --fold 0 --dataloader_num_workers 48 --learning_rate 8e-5 --num_train_epochs 40 --per_device_train_batch_size 768 --per_device_eval_batch_size 768 --remove_unused_columns False --load_best_model_at_end --objective siamese --max_len 128 --is_sentence_transformers --top_k_neighbors 50 --report_to --gradient_accumulation_steps 4 none --overwrite_output_dir
```




# TODO:
1. Embedding
- [x] Add all positive pairs to the training set
- [x] Add pair content-content
- [x] SentenceBert Softmax loss: https://arxiv.org/pdf/1908.10084.pdf
- [x] Training with content texts
- [x] KNN instead of annoy for retrieve embeddings
- [x] Add parent and child topic to topic text
- [x] Add text information to content
- [x] Hard negatives: https://www.kaggle.com/competitions/learning-equality-curriculum-recommendations/discussion/376873
- [x] Try another loss function: https://www.sbert.net/docs/package_reference/losses.html#cosinesimilarityloss
- [x] 2 stages pipeline: https://www.sbert.net/examples/applications/retrieve_rerank/README.html. https://www.sbert.net/examples/applications/cross-encoder/README.html
- [x] Supervised dataset generation loop: 
    1. Generate from pretrained model
    2. Train new embedding - retriever (then calculate top-k max postitive score)
    3. Get top-k to generate new pairs, repeat step 2 (until top-k max postitive score doesn't change much, go to step 4)
    4. Train classifier to get last classifier - reranking.
    Note: or we can change top-k dataset pairs every epoch: https://stackoverflow.com/questions/72750887/how-to-update-training-dataset-at-epoch-begin-in-huggingface-trainer-using-callb
- [x] Leave the context: parents + children of topics as a separated information in tokenizer.encode (consider it as a second sequence) => not working
- [x] Add grandparents, grandchildren info
- [x] Pretrained Cross Encoder: https://www.sbert.net/docs/pretrained_cross-encoders.html
- [ ] Pretrained using translation: https://www.sbert.net/examples/training/multilingual/README.html
- [x] Pretrained using pair translation:
    - [x] Only add positive cases in training set for translated topics
    - [x] Only original contents for original topics
    - [x] Only evaluate (KNN) with original contents
- [x] Augmentation text data. i,e using [MASK] => not working
    ```
    probability_matrix = torch.full(inputs["input_ids"].shape, 0.15)
    masked_indices = torch.bernoulli(probability_matrix).bool()
    indices_replaced = torch.bernoulli(torch.full(inputs["input_ids"].shape, 0.8)).bool() & masked_indices
    inputs["input_ids"][indices_replaced] = tokenizer.convert_tokens_to_ids(tokenizer.mask_token)
    ```
- [x] Leave the context: parents + children of topics as a separated information in tokenizer.encode (consider it as a second sequence) => not working
- [x] Add grandparents, grandchildren info
- [ ] Test/Validation phase: add all train topic titles to content descriptions in validation/test phase to see if it improves the result. If we add it in training phase, the model maybe overfitted, but let's try.
- [x] Add parents and childs information before description of titles because of the description may be long. => not working
- [ ] Experiment with gradient checkpointing
- [ ] Experiment with gradient_accumulation_steps
- [ ] Batch sampling: make pairs have same topics in the same batch
- [ ] Embedding of last N blocks
- [ ] Triplet loss

2. Classification
- [x] KFold XGBoost
- [ ] BM25 retrieval for filtering?
- [ ] Add Siamese embeddings to classification models
- [ ] Merge 2 stages and train end2end pipeline
- [ ] Add f2 score directly to evaluation epoch
- [x] Swap order when training classification model for augmentation
- [ ] Add title of nearest content to topic text, then retrieve again / or retrieve nearest of that content.

# Generate negative data based on this:
1. https://www.kaggle.com/code/ragnar123/lecr-unsupervised-train-set-public
2. https://www.kaggle.com/code/ragnar123/lecr-xlm-roberta-base-baseline

# Resources
1. https://www.kaggle.com/code/kaizen97/sbert-fuzzy-annoy/comments
2. https://www.kaggle.com/code/ragnar123/lecr-xlm-roberta-base-baseline
3. Contrastive loss: https://towardsdatascience.com/how-to-choose-your-loss-when-designing-a-siamese-neural-net-contrastive-triplet-or-quadruplet-ecba11944ec
4. https://www.kaggle.com/competitions/learning-equality-curriculum-recommendations/discussion/375313
5. https://github.com/openai/whisper/blob/28769fcfe50755a817ab922a7bc83483159600a9/whisper/tokenizer.py#L295