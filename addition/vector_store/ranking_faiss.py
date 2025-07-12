from sentence_transformers import SentenceTransformer
from utils.config import SQLITE_DB_PATH
from fastapi import FastAPI, Query
import sqlite3, joblib
import pandas as pd
import  os
from utils.middleware_cors_config import add_cors 
import json
import faiss


app = FastAPI()
add_cors(app)

@app.post("/ranking_faiss")
def ranking_faiss(dataset: str = Query(...), query_id: str = Query(...), top_k: int = Query(10)):
    query_path = f"utils/joblib_files/query_vectors/{dataset}_embedding_{query_id}.joblib"
    if not os.path.exists(query_path):
        return {"error": f"Query vector not found for {query_id}"}
    query_vec = joblib.load(query_path)["query_vector"].astype("float32")

    index_path = f"utils/faiss_indexes/{dataset}_embedding.index"
    if not os.path.exists(index_path):
        return {"error": f"FAISS index not found for {dataset}"}
    index = faiss.read_index(index_path)

    meta_path = f"utils/faiss_indexes/{dataset}_embedding_meta.json"
    if not os.path.exists(meta_path):
        return {"error": "Index metadata not found"}
    with open(meta_path, "r", encoding="utf-8") as f:
        doc_ids = json.load(f)

    scores, indices = index.search(query_vec, top_k)

    results = []
    for i in range(len(indices[0])):
        doc_index = indices[0][i]
        if doc_index < len(doc_ids):
            results.append({
                "doc_id": doc_ids[doc_index],
                "score": float(scores[0][i])
            })

    return {"results": results}
