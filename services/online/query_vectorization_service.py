from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI()

vectorizer, _, _ = joblib.load("utils/joblib_files/tfidf_model/vectorizer.joblib")

class CleanedQuery(BaseModel):
    cleaned_text: str

@app.post("/vectorize")
def vectorize(cleaned: CleanedQuery):
    vec = vectorizer.transform([cleaned.cleaned_text])
    return {"vector": vec.toarray().tolist()}