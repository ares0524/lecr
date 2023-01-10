# clean text
import re
import string


def decontracted(phrase):

    # Specific
    phrase = re.sub(r"won't", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)
    # ..

    # General
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    # ..

    return phrase

def remove_punctuations(text):
    for punctuation in list(string.punctuation): text = text.replace(punctuation, '')
    return text

def clean_number(text):
    text = re.sub(r'(\d+)([a-zA-Z])', '\g<1> \g<2>', text)
    text = re.sub(r'(\d+) (th|st|nd|rd) ', '\g<1>\g<2> ', text)
    text = re.sub(r'(\d+),(\d+)', '\g<1>\g<2>', text)
    return text

def clean_whitespace(text):
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text

def clean_repeat_words(text):
    return re.sub(r"(\w*)(\w)\2(\w*)", r"\1\2\3", text)

def clean_text(text):
    text = str(text)
    text = decontracted(text)
    text = remove_punctuations(text)
    text = clean_number(text)
    text = clean_whitespace(text)
    
    return text