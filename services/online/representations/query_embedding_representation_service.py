from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import os
from sentence_transformers import SentenceTransformer
from typing import List
from utils.middleware_cors_config import add_cors 

app = FastAPI()
add_cors(app)

class CleanedQuery(BaseModel):
    query_tokens: List[str]
    dataset_name: str
    query_id: str  


@app.post("/vectorize_embedding")
def vectorize_embedding(cleaned: CleanedQuery):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode([cleaned.query_tokens])

    save_path = f"utils/joblib_files/query_vectors/{cleaned.dataset_name}_embedding_{cleaned.query_id}.joblib"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    joblib.dump({"query_vector": embedding}, save_path)

    return {"vector": embedding.tolist(), "saved_to": save_path}
