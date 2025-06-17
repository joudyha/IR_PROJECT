from fastapi import FastAPI
from pydantic import BaseModel
import joblib, os
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List
from utils.middleware_cors_config import add_cors 

app = FastAPI()
add_cors(app)

class CleanedQuery(BaseModel):
    query_tokens: List[str]
    dataset_name: str
    query_id: str  # أضفنا هذا لحفظ ملف الاستعلام

@app.post("/vectorize_hybrid")
def vectorize_hybrid(cleaned: CleanedQuery):
    # 1. Load hybrid model (to get the TF-IDF vectorizer)
    hybrid_model_path = f"utils/joblib_files/hybrid_model/{cleaned.dataset_name}_hybrid.joblib"
    if not os.path.exists(hybrid_model_path):
        return {"error": f"Hybrid model not found for {cleaned.dataset_name}"}
    
    hybrid_model = joblib.load(hybrid_model_path)
    tfidf_vectorizer = hybrid_model["tfidf_vectorizer"]

    # 2. Compute TF-IDF vector
    tfidf_vec = tfidf_vectorizer.transform([" ".join(cleaned.query_tokens)]).toarray()

    # 3. Compute BERT embedding
    model = SentenceTransformer('all-MiniLM-L6-v2')
    emb_vec = model.encode([" ".join(cleaned.query_tokens)])

    # 4. Concatenate both vectors to form hybrid vector
    hybrid_vec = np.hstack((tfidf_vec, emb_vec))

    # 5. Save query vector
    save_path = f"utils/joblib_files/query_vectors/{cleaned.dataset_name}_hybrid_{cleaned.query_id}.joblib"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    joblib.dump({"query_vector": hybrid_vec}, save_path)

    return {
        "vector": hybrid_vec.tolist(),
        "saved_to": save_path
    }
