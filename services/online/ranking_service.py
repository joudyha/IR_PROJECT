
from fastapi import FastAPI
from pydantic import BaseModel
import joblib, os
from typing import List
from utils.middleware_cors_config import add_cors
from sentence_transformers import CrossEncoder
from utils.retrieval import (
    load_inverted_index,
    get_candidate_docs,
    rank_with_cosine,
    rank_with_bm25,
)

cross_encoder = CrossEncoder("utils/Bert_model/ms-marco-MiniLM-L-6-v2")


app = FastAPI()
add_cors(app)

class RankRequest(BaseModel):
    dataset: str
    representation: str  
    query_id: str
  
@app.post("/rank")
def rank_documents(req: RankRequest):
    rep = req.representation.lower()

    query_path = f"utils/joblib_files/query_vectors/{req.dataset}_{rep}_{req.query_id}.joblib"
    if not os.path.exists(query_path):
        return {"error": "Query vector not found"}
    query_data = joblib.load(query_path)

    doc_path = f"utils/joblib_files/{rep}_model/{req.dataset}_{rep}.joblib"
    if not os.path.exists(doc_path):
        return {"error": "Document vectors not found"}
    doc_data = joblib.load(doc_path)
    doc_ids = doc_data["doc_ids"]

    ranked = []

    if rep in ["tfidf", "embedding", "hybrid"]:
        doc_vecs = doc_data["vectors"] if rep == "tfidf" else (
            doc_data["embeddings"] if rep == "embedding" else doc_data["hybrid_vectors"]
        )
        query_vec = query_data["query_vector"]

        if rep == "tfidf":
            try:
                index = load_inverted_index(req.dataset)
                query_tokens = query_data.get("query_tokens", [])
                candidate_ids = get_candidate_docs(query_tokens, index)
                doc_id_to_index = {doc_id: i for i, doc_id in enumerate(doc_ids)}
                candidate_indices = [doc_id_to_index[doc_id] for doc_id in candidate_ids if doc_id in doc_id_to_index]
                
                if candidate_indices:
                    doc_vecs = doc_vecs[candidate_indices]
                    doc_ids = candidate_ids
            except FileNotFoundError:
                pass 

        ranked = rank_with_cosine(query_vec, doc_vecs, doc_ids)
        
        if rep == "embedding":
            top_n = 50 
            raw_query = query_data["raw_query"]
            raw_docs = doc_data["raw_docs"]
            top_docs = ranked[:top_n]

            pairs = [(raw_query, raw_docs[doc_id]) for doc_id, _ in top_docs]
            cross_scores = cross_encoder.predict(pairs)

            reranked = sorted(zip(top_docs, cross_scores), key=lambda x: x[1], reverse=True)
            ranked = [(doc_id, float(score)) for ((doc_id, _), score) in reranked]


    elif rep == "bm25":
        bm25_vectorizer = doc_data["bm25"]
        query_tokens = query_data["query_tokens"]

        index = load_inverted_index(req.dataset)
        candidate_ids = get_candidate_docs(query_tokens, index)
        doc_id_to_index = {doc_id: i for i, doc_id in enumerate(doc_ids)}
        candidate_indices = [doc_id_to_index[doc_id] for doc_id in candidate_ids if doc_id in doc_id_to_index]

        ranked = rank_with_bm25(query_tokens, bm25_vectorizer, doc_ids, candidate_indices)

    else:
        return {"error": f"Unsupported representation: {rep}"}


    top_k = [{"doc_id": doc_id, "score": float(score)} for doc_id, score in ranked[:10]]
    return {
        "representation": rep,
        "dataset": req.dataset,
        "results": top_k
    }
