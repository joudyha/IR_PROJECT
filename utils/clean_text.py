import re
import string
import datefinder
import contractions
import country_converter as coco
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from datetime import datetime



lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    return wordnet.NOUN

contractions_dict = {
    "u": "you",
    "r": "are",
    "wanna": "want to",
    "can't": "cannot",
    "don't": "do not",
    "didn't": "did not",
    "it's": "it is",
    "i'm": "i am",
}

def expand_contractions(text, contractions_dict):
    pattern = re.compile(r'\b(' + '|'.join(re.escape(key) for key in contractions_dict.keys()) + r')\b')
    return pattern.sub(lambda x: contractions_dict[x.group()], text)


def processing(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = expand_contractions(text, contractions_dict)
    text = text.encode("ascii", errors="ignore").decode()  
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)   
    text = re.sub(r"\S+@\S+", "", text)                     
    text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)  
    text = re.sub(r"\b\d{1,2}\b", "", text)                 
    text = re.sub(r"\b\d{5,}\b", "", text)               
    return text

def tokenize(text):
    tokens = word_tokenize(text)
    tokens_pos = pos_tag(tokens)
    lemmatized = [
        lemmatizer.lemmatize(word, get_wordnet_pos(pos))
        for word, pos in tokens_pos
        if word not in stop_words and len(word) > 1
    ]
    return lemmatized


def clean_text(text):
    preprocessing = processing(text)
    tokenizing = tokenize(preprocessing)
    return tokenizing

def light_clean(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"\S+@\S+", "", text)
    text = text.encode("ascii", errors="ignore").decode()
    text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text




