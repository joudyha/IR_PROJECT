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

# @app.post("/run_query_hybrid")
# async def run_query_hybrid(req: QueryRequest):
#     qid = get_next_qid()
#     async with httpx.AsyncClient(timeout=30.0) as client:
#         step1 = await client.post(SERVICES_URL["CLEAN_QUERY"], json={"query": req.query})
#         if step1.status_code != 200:
#             return {"error": "clean_query failed", "detail": step1.text}
#         query_tokens = step1.json()["query_tokens"]

#         step2 = await client.post(SERVICES_URL["Vectorize_Hybrid"], json={
#             "query_tokens": query_tokens,
#             "dataset_name": req.dataset_name,
#             "query_id": qid
#         })
#         if step2.status_code != 200:
#             return {"error": "vectorization failed", "detail": step2.text}

#         step3 = await client.post(SERVICES_URL["Ranking"], json={
#             "representation": "hybrid",
#             "dataset": req.dataset_name,
#             "query_id": qid
#         })
#         if step3.status_code != 200:
#             return {"error": "ranking failed", "detail": step3.text}

#   # 4. جلب النصوص فقط بدون السكور
#         doc_ids = [item["doc_id"] for item in step3.json().get("results", [])]
#         step4 = await client.post(SERVICES_URL["GET_DOCS_TEXTS"], json={
#             "dataset_name": req.dataset_name,
#             "doc_ids": doc_ids
#         })
#         if step4.status_code != 200:
#             return {"error": "get_docs_texts failed", "detail": step4.text}

#     # نرجع فقط النصوص مع doc_id
#     return {
#         "texts": step4.json().get("texts", [])
#     }

@app.post("/run_query_hybrid")
async def run_query_hybrid(req: QueryRequest):
    qid = get_next_qid()
    async with httpx.AsyncClient(timeout=30.0) as client:
        # خطوة التنظيف الهجين
        step1 = await client.post(SERVICES_URL["HYBRID_CLEAN_QUERY"], json={"query": req.query})
        if step1.status_code != 200:
            return {"error": "clean_query failed", "detail": step1.text}
        
        data = step1.json()
        heavy_tokens = data.get("heavy_tokens", [])
        light_tokens = data.get("light_tokens", [])
        light_text = data.get("light_text", "")

        # خطوة التمثيل الهجين
        step2 = await client.post(SERVICES_URL["Vectorize_Hybrid"], json={
            "heavy_tokens": heavy_tokens,
            "light_tokens": light_tokens,
            "light_text": light_text,
            "dataset_name": req.dataset_name,
            "query_id": qid
        })
        if step2.status_code != 200:
            return {"error": "vectorization failed", "detail": step2.text}

        # خطوة الترتيب
        step3 = await client.post(SERVICES_URL["Ranking"], json={
            "representation": "hybrid",
            "dataset": req.dataset_name,
            "query_id": qid
        })
        if step3.status_code != 200:
            return {"error": "ranking failed", "detail": step3.text}

        # جلب نصوص المستندات فقط بدون السكور
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
