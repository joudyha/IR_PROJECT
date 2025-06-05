def clean_text(text: str) -> str:
    if not text:
        return ""

    import re
    import string
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer
    import nltk
    nltk.download('stopwords', quiet=True)
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()

    text = text.lower()
    text = re.sub(rf"[{string.punctuation}]", "", text)
    words = text.split()
    words = [stemmer.stem(word) for word in words if word not in stop_words]
    return " ".join(words)
