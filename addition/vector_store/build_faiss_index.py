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

@app.post("/build_faiss_index")
def build_faiss_index(dataset_name: str = Query(...), index_type: str = Query("Flat")):
    vector_path = f"utils/joblib_files/embedding_model/{dataset_name}_embedding.joblib"
    
    if not os.path.exists(vector_path):
        return {"error": f"Vector file not found at: {vector_path}"}

    data = joblib.load(vector_path)
    vectors = data["embeddings"]
    doc_ids = data["doc_ids"]

    if len(vectors) == 0:
        return {"error": "No vectors to index."}

    dim = vectors.shape[1]

    if index_type == "Flat":
        index = faiss.IndexFlatL2(dim)
    elif index_type == "IVF":
        quantizer = faiss.IndexFlatL2(dim)
        index = faiss.IndexIVFFlat(quantizer, dim, 100)
        index.train(vectors)
    else:
        return {"error": f"Unknown index type: {index_type}"}

    index.add(vectors)

    os.makedirs("utils/faiss_indexes", exist_ok=True)

    faiss.write_index(index, f"utils/faiss_indexes/{dataset_name}_embedding.index")
    with open(f"utils/faiss_indexes/{dataset_name}_embedding_meta.json", "w", encoding="utf-8") as f:
        json.dump(doc_ids, f, ensure_ascii=False)

    return {
        "status": "✅ FAISS index created and saved.",
        "documents_indexed": len(doc_ids),
        "index_type": index_type
    }
