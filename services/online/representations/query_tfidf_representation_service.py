from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import os
from typing import List 
from utils.middleware_cors_config import add_cors 





app = FastAPI()
add_cors(app)

class CleanedQuery(BaseModel):
    query_tokens:List[str]
    dataset_name: str
    query_id: str 

@app.post("/vectorize_tfidf")
def vectorize(cleaned: CleanedQuery):
    model_path = f"utils/joblib_files/tfidf_model/{cleaned.dataset_name}_tfidf.joblib"

    if not os.path.exists(model_path):
        return {"error": f"Model for dataset '{cleaned.dataset_name}' not found."}


    model = joblib.load(model_path)
    vectorizer = model["vectorizer"]

    vec = vectorizer.transform([" ".join(cleaned.query_tokens)])

    save_path = f"utils/joblib_files/query_vectors/{cleaned.dataset_name}_tfidf_{cleaned.query_id}.joblib"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    joblib.dump({
        "query_vector": vec,
        "query_tokens":cleaned.query_tokens
    }, save_path)

    return {"vector": vec.toarray().tolist(),"query_tokens": cleaned.query_tokens, "saved_to": save_path}
