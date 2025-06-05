from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = FastAPI()

_, tfidf_matrix, doc_ids = joblib.load("utils/joblib_files/tfidf_model/vectorizer.joblib")

class VectorInput(BaseModel):
    vector: list

@app.post("/rank")
def rank_docs(vec_input: VectorInput):
    vec = np.array(vec_input.vector)
    sim_scores = cosine_similarity(vec, tfidf_matrix).flatten()
    ranked = sorted(zip(doc_ids, sim_scores), key=lambda x: x[1], reverse=True)[:5]
    return {"top_docs": ranked}