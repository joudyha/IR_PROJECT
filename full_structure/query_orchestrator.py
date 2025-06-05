from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/query_pipeline")
def full_pipeline(input: QueryRequest):
    # 1. Clean
    cleaned = requests.post("http://localhost:8010/clean", json={"query": input.query}).json()["cleaned_text"]
    
    # 2. Vectorize
    vector = requests.post("http://localhost:8011/vectorize", json={"cleaned_text": cleaned}).json()["vector"]
    
    # 3. Rank
    ranked = requests.post("http://localhost:8012/rank", json={"vector": vector}).json()["top_docs"]
    
    return {"cleaned_text": cleaned, "top_docs": ranked}