# 
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import os
from sentence_transformers import SentenceTransformer
from typing import List
from utils.middleware_cors_config import add_cors 

app = FastAPI()
add_cors(app)

model = SentenceTransformer('D:/GRADUATE/IR_Project_LFE/utils/Bert_model/all-MiniLM-L6-v2')

class CleanedQuery(BaseModel):
    query_tokens: List[str]
    dataset_name: str
    query_id: str  
    raw_query:str


@app.post("/vectorize_embedding")
def vectorize_embedding(cleaned: CleanedQuery):
    embedding = model.encode([" ".join(cleaned.query_tokens)])

    save_path = f"utils/joblib_files/query_vectors/{cleaned.dataset_name}_embedding_{cleaned.query_id}.joblib"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    joblib.dump({"query_vector": embedding,
        "raw_query": cleaned.raw_query,
        "query_tokens": cleaned.query_tokens}
        , save_path)

    return {"vector": embedding.tolist(), "saved_to": save_path}
