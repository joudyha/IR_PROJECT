import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk
import contractions

# تحميل الموارد المطلوبة
# nltk.download('punkt', quiet=True)
# nltk.download('stopwords', quiet=True)
# nltk.download('averaged_perceptron_tagger', quiet=True)
# nltk.download('wordnet', quiet=True)

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))
custom_stopwords = {
    "like", "also", "just", "get", "got", "use", "used", "using", "really", "would",
    "could", "should", "think", "say", "said", "even", "etc", "one", "go", "going",
    "thing", "things", "know", "see", "many", "much", "way", "still"
}
stop_words |= custom_stopwords

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



def expand_contractions(text):
    return contractions.fix(text)

# تابع التنظيف الأساسي
def processing(text: str) -> str:
    print("📌 Preprocessing...")
    if not text:
        return ""
    text = contractions.fix(text)
    text = text.lower()
    text = text.encode("ascii", errors="ignore").decode()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"\S+@\S+", "", text)
    text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)
    text = re.sub(r"\d+", "", text)
    return text 

# تابع التقطيع + lemmatization
def tokenize(text):
    print("✂️ Tokenizing...")
    tokens = word_tokenize(text)
    tokens_pos = pos_tag(tokens)
    lemmatized = [
        lemmatizer.lemmatize(word, get_wordnet_pos(pos))
        for word, pos in tokens_pos
        if word not in stop_words and len(word) > 2
    ]
    return lemmatized


def clean_text(text):
    preprocessing=processing(text)
    tokenizing=tokenize(preprocessing)
    return tokenizing