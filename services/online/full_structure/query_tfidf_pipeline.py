from fastapi import FastAPI
from pydantic import BaseModel
import httpx
from utils.config import SERVICES_URL
from utils.middleware_cors_config import add_cors 
from utils.retrieval import get_next_qid

app = FastAPI()
add_cors(app)

class QueryRequest(BaseModel):
    query: str
    dataset_name: str
@app.post("/run_query_tfidf")
async def run_query_tfidf(req: QueryRequest):
    qid = get_next_qid()
    async with httpx.AsyncClient(timeout=60.0) as client:
        # Step 1: تنظيف الاستعلام
        step1 = await client.post(SERVICES_URL["CLEAN_QUERY"], json={"query": req.query})
        if step1.status_code != 200:
            return {"error": "clean_query failed", "detail": step1.text}
        query_tokens = step1.json()["query_tokens"]

        # Step 2: تحويل إلى تمثيل tf-idf
        step2 = await client.post(SERVICES_URL["Vectorize_Tfidf"], json={
            "query_tokens": query_tokens,
            "dataset_name": req.dataset_name,
            "query_id": qid
        })
        if step2.status_code != 200:
            return {"error": "vectorization failed", "detail": step2.text}

        # Step 3: الترتيب
        step3 = await client.post(SERVICES_URL["Ranking"], json={
            "representation": "tfidf",
            "dataset": req.dataset_name,
            "query_id": qid
        })
        if step3.status_code != 200:
            return {"error": "ranking failed", "detail": step3.text}

     # 4. جلب النصوص فقط بدون السكور
        doc_ids = [item["doc_id"] for item in step3.json().get("results", [])]
        step4 = await client.post(SERVICES_URL["GET_DOCS_TEXTS"], json={
            "dataset_name": req.dataset_name,
            "doc_ids": doc_ids
        })
        if step4.status_code != 200:
            return {"error": "get_docs_texts failed", "detail": step4.text}
    # نرجع فقط النصوص مع doc_id
    return {
        "texts": step4.json().get("texts", [])
    }
