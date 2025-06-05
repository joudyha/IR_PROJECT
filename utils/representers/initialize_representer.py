from .tfidf_representer import TfidfRepresenter
# utils/representers/__init__.py

def get_representer(representation_type: str, dataset_name: str):
    if representation_type.lower() == "tfidf":
        return TfidfRepresenter(dataset_name)
    # ممكن تضيف: count, embedding, إلخ
    return None
