from fastapi import FastAPI
from pydantic import BaseModel
import joblib, os
from typing import List
from utils.middleware_cors_config import add_cors 
from utils.retrieval import (
    load_inverted_index,
    get_candidate_docs,
    rank_with_cosine,
    rank_with_bm25,
)

app = FastAPI()
add_cors(app)

class RankRequest(BaseModel):
    dataset: str
    representation: str  # tfidf, embedding, bm25, hybrid
    query_id: str

@app.post("/rank")
def rank_documents(req: RankRequest):
    rep = req.representation.lower()

    # 1. تحميل تمثيل الاستعلام
    query_path = f"utils/joblib_files/query_vectors/{req.dataset}_{rep}_{req.query_id}.joblib"
    if not os.path.exists(query_path):
        return {"error": "Query vector not found"}
    query_data = joblib.load(query_path)

    # 2. تحميل تمثيل المستندات
    doc_path = f"utils/joblib_files/{rep}_model/{req.dataset}_{rep}.joblib"
    if not os.path.exists(doc_path):
        return {"error": "Document vectors not found"}
    doc_data = joblib.load(doc_path)
    doc_ids = doc_data["doc_ids"]

    # 3. تطبيق حسب نوع التمثيل
    if rep in ["tfidf", "embedding", "hybrid"]:
        doc_vecs = doc_data["vectors"] if rep == "tfidf" else (
            doc_data["embeddings"] if rep == "embedding" else doc_data["hybrid_vectors"]
        )
        query_vec = query_data["query_vector"]

        # لو بدنا نستخدم inverted index
        if rep in ["tfidf"]:  # ممكن تعملها لأي نوع إذا بدك
            index = load_inverted_index(req.dataset)
            query_tokens = query_data.get("query_tokens", [])
            candidate_ids = get_candidate_docs(query_tokens, index)
            doc_id_to_index = {doc_id: i for i, doc_id in enumerate(doc_ids)}
            candidate_indices = [doc_id_to_index[doc_id] for doc_id in candidate_ids if doc_id in doc_id_to_index]
            doc_vecs = doc_vecs[candidate_indices]
            doc_ids = candidate_ids

        ranked = rank_with_cosine(query_vec, doc_vecs, doc_ids)

    elif rep == "bm25":
        tokenized_corpus = doc_data["tokenized_corpus"]
        query_tokens = query_data["query_tokens"]

        index = load_inverted_index(req.dataset)
        candidate_ids = get_candidate_docs(query_tokens, index)
        doc_id_to_index = {doc_id: i for i, doc_id in enumerate(doc_ids)}
        candidate_indices = [doc_id_to_index[doc_id] for doc_id in candidate_ids if doc_id in doc_id_to_index]

        ranked = rank_with_bm25(query_tokens, tokenized_corpus, doc_ids, candidate_indices)

    else:
        return {"error": f"Unsupported representation: {rep}"}

    # 4. إعادة النتائج
    top_k = [{"doc_id": doc_id, "score": float(score)} for doc_id, score in ranked[:10]]
    return {
        "representation": rep,
        "dataset": req.dataset,
        "results": top_k
    }
