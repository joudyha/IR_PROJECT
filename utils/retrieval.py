import json
import os
import joblib
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi

def load_inverted_index(dataset_name: str):
    path = f"utils/inverted_index/{dataset_name}_index.json"
    if not os.path.exists(path):
        raise FileNotFoundError("Inverted index not found")
    with open(path, "r") as f:
        return json.load(f)

def get_candidate_docs(query_tokens: list, inverted_index: dict):
    doc_ids = set()
    for token in query_tokens:
        if token in inverted_index:
            doc_ids.update(inverted_index[token])
    return list(doc_ids)

def rank_with_cosine(query_vec, doc_vecs, doc_ids):
    sims = cosine_similarity(query_vec, doc_vecs)[0]
    return sorted(zip(doc_ids, sims), key=lambda x: x[1], reverse=True)

def rank_with_bm25(query_tokens, tokenized_corpus, doc_ids, candidate_indices=None):
    bm25 = BM25Okapi(tokenized_corpus)
    scores = bm25.get_scores(query_tokens)

    if candidate_indices is not None:
        filtered_scores = [(doc_ids[i], scores[i]) for i in candidate_indices]
        return sorted(filtered_scores, key=lambda x: x[1], reverse=True)
    else:
        return sorted(zip(doc_ids, scores), key=lambda x: x[1], reverse=True)

counter = 0
def get_next_qid():
    global counter
    qid = f"Q{counter}"
    counter += 1
    return qid
