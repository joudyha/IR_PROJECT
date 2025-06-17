from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import os
from typing import List
from utils.middleware_cors_config import add_cors 
app = FastAPI()
add_cors(app)

class CleanedQuery(BaseModel):
    query_tokens: List[str]
    dataset_name: str
    query_id: str  # 👈 نضيف معرف للاستعلام حتى نخزنه باسم مميز


@app.post("/vectorize_bm25")
def save_query_bm25(cleaned: CleanedQuery):
    save_path = f"utils/joblib_files/query_vectors/{cleaned.dataset_name}_bm25_{cleaned.query_id}.joblib"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    joblib.dump({"query_tokens": cleaned.query_tokens}, save_path)

    return {"query_tokens": cleaned.query_tokens, "saved_to": save_path}
