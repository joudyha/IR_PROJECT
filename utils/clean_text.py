import re
import string
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import nltk
from nltk import WordNetLemmatizer, pos_tag
from nltk.corpus import stopwords
from nltk.corpus import wordnet
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('stopwords', )
nltk.download('averaged_perceptron_tagger_eng')



def get_wordnet_pos(tag_parameter):
    tag = tag_parameter[0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)

def clean_text(text: str) -> str:
    if not text:
        return ""
    stop_words = set(stopwords.words('english'))
    # stemmer = PorterStemmer()
    text = text.lower()
    text = re.sub(rf"[{string.punctuation}]", "", text)
    words = text.split()
    tokens = [item for item in words if item not in stop_words]
    tokens = pos_tag(tokens)
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word, pos=get_wordnet_pos(tag)) for word, tag, in tokens]
    # words = [stemmer.stem(word) for word in words if word not in stop_words]
    return " ".join(lemmatized_words)
