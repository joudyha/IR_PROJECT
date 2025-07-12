# # from fastapi import FastAPI
# # from pydantic import BaseModel
# # import httpx
# # from utils.config import SERVICES_URL
# # from utils.middleware_cors_config import add_cors 
# # from utils.retrieval import get_next_qid
# # import time

# # app = FastAPI()
# # add_cors(app)

# # class QueryRequest(BaseModel):
# #     query: str
# #     dataset_name: str
# #     method: str = "default"  # default or faiss

# # @app.post("/run_query_embedding")
# # async def run_query_embedding(req: QueryRequest):
# #     qid = get_next_qid()
# #     async with httpx.AsyncClient(timeout=30.0) as client:
# #         step1 = await client.post(SERVICES_URL["LIGHT_CLEAN_QUERY"], json={"query": req.query})
# #         if step1.status_code != 200:
# #             return {"error": "clean_query failed", "detail": step1.text}
# #         query_tokens = step1.json()["query_tokens"]

# #         step2 = await client.post(SERVICES_URL["Vectorize_Embedding"], json={
# #             "query_tokens": query_tokens,
# #             "dataset_name": req.dataset_name,
# #             "query_id": qid,
# #             "raw_query": req.query  # 

# #         })
# #         if step2.status_code != 200:
# #             return {"error": "vectorization failed", "detail": step2.text}
# #         print("step3 running")
# #         ranking_url = SERVICES_URL["Ranking_FAISS"] if req.method.lower() == "faiss" else SERVICES_URL["Ranking"]
# #         if req.method.lower() == "faiss":
# #             start = time.time()
# #             step3 = await client.post(ranking_url, params={
# #                 "dataset": req.dataset_name,
# #                 "query_id": qid,
# #                 "top_k": 10
# #             })

# #             end=time.time()
# #             print(f"⏱️ faiss_time : {end - start:.4f} s")

# #         else:
# #             start = time.time()
# #             step3 = await client.post(ranking_url, json={
# #                 "representation": "embedding",
# #                 "dataset": req.dataset_name,
# #                 "query_id": qid,
# #                 "top_k": 10
# #             })
# #             end=time.time()
# #             print(f"⏱️ cosine_time : {end - start:.4f} s")

# #         if step3.status_code != 200:
# #             return {"error": "ranking failed", "detail": step3.text}
# #         print("step3 done")

# #         doc_ids = [item["doc_id"] for item in step3.json().get("results", [])]
# #         step4 = await client.post(SERVICES_URL["GET_DOCS_TEXTS"], json={
# #             "dataset_name": req.dataset_name,
# #             "doc_ids": doc_ids
# #         })
# #         if step4.status_code != 200:
# #             return {"error": "get_docs_texts failed", "detail": step4.text}

# #     return {
# #         "texts": step4.json().get("texts", [])
# #     }




# from fastapi import FastAPI
# from pydantic import BaseModel
# import httpx
# from utils.config import SERVICES_URL
# from utils.middleware_cors_config import add_cors 
# from utils.retrieval import get_next_qid
# import time

# app = FastAPI()
# add_cors(app)

# class QueryRequest(BaseModel):
#     query: str
#     dataset_name: str
#     method: str = "default"  # default or faiss
#     chosen_option: str = "original"  # original, corrected, expanded

# @app.post("/run_query_embedding")
# async def run_query_embedding(req: QueryRequest):
#     qid = get_next_qid()
#     async with httpx.AsyncClient(timeout=30.0) as client:

#         # 1. جلب الاقتراحات
#         suggestion_res = await client.post(SERVICES_URL["SUGGESTIONS"], json={
#             "query": req.query,
#             "dataset_name": req.dataset_name
#         })
#         if suggestion_res.status_code != 200:
#             return {"error": "suggestions failed", "detail": suggestion_res.text}
#         suggestion_data = suggestion_res.json()

#         # 2. بناء الاستعلام النهائي حسب خيار المستخدم
#         if req.chosen_option == "corrected":
#             final_query = suggestion_data.get("corrected_query", req.query)
#         elif req.chosen_option == "expanded":
#             final_query = suggestion_data.get("expanded_query", req.query)
#         else:
#             final_query = req.query

#         # 3. تنظيف الاستعلام النهائي
#         step1 = await client.post(SERVICES_URL["LIGHT_CLEAN_QUERY"], json={"query": final_query})
#         if step1.status_code != 200:
#             return {"error": "clean_query failed", "detail": step1.text}
#         query_tokens = step1.json()["query_tokens"]

#         # 4. التمثيل (vectorization)
#         step2 = await client.post(SERVICES_URL["Vectorize_Embedding"], json={
#             "query_tokens": query_tokens,
#             "dataset_name": req.dataset_name,
#             "query_id": qid,
#             "raw_query": final_query
#         })
#         if step2.status_code != 200:
#             return {"error": "vectorization failed", "detail": step2.text}

#         # 5. الرتبة (Ranking)
#         ranking_url = SERVICES_URL["Ranking_FAISS"] if req.method.lower() == "faiss" else SERVICES_URL["Ranking"]
#         start = time.time()
#         if req.method.lower() == "faiss":
#             step3 = await client.post(ranking_url, params={
#                 "dataset": req.dataset_name,
#                 "query_id": qid,
#                 "top_k": 10
#             })
#         else:
#             step3 = await client.post(ranking_url, json={
#                 "representation": "embedding",
#                 "dataset": req.dataset_name,
#                 "query_id": qid,
#                 "top_k": 10
#             })
#         end = time.time()
#         print(f"⏱️ ranking_time : {end - start:.4f} s")

#         if step3.status_code != 200:
#             return {"error": "ranking failed", "detail": step3.text}

#         # 6. جلب نصوص المستندات المرتبة
#         doc_ids = [item["doc_id"] for item in step3.json().get("results", [])]
#         step4 = await client.post(SERVICES_URL["GET_DOCS_TEXTS"], json={
#             "dataset_name": req.dataset_name,
#             "doc_ids": doc_ids
#         })
#         if step4.status_code != 200:
#             return {"error": "get_docs_texts failed", "detail": step4.text}

#     return {
#         "texts": step4.json().get("texts", [])
#     }


# from fastapi import FastAPI
# from pydantic import BaseModel
# import httpx
# from utils.config import SERVICES_URL
# from utils.middleware_cors_config import add_cors 
# from utils.retrieval import get_next_qid
# import time

# app = FastAPI()
# add_cors(app)

# class QueryRequest(BaseModel):
#     query: str
#     dataset_name: str
#     method: str = "default"  # default or faiss
#     chosen_option: str = "original"  # original, corrected, expanded

# @app.post("/run_query_embedding")
# async def run_query_embedding(req: QueryRequest):
#     qid = get_next_qid()
#     async with httpx.AsyncClient(timeout=30.0) as client:

#         # 1. جلب الاقتراحات
#         suggestion_res = await client.post(SERVICES_URL["SUGGESTIONS"], json={
#             "query": req.query,
#             "dataset_name": req.dataset_name
#         })
#         if suggestion_res.status_code != 200:
#             return {"error": "suggestions failed", "detail": suggestion_res.text}
#         suggestion_data = suggestion_res.json()

#         # 2. بناء الاستعلام النهائي حسب خيار المستخدم
#         if req.chosen_option == "corrected":
#             final_query = suggestion_data.get("corrected_query", req.query)
#         elif req.chosen_option == "expanded":
#             final_query = suggestion_data.get("expanded_query", req.query)
#         else:
#             final_query = req.query

#         # 3. تنظيف الاستعلام النهائي
#         step1 = await client.post(SERVICES_URL["LIGHT_CLEAN_QUERY"], json={"query": final_query})
#         if step1.status_code != 200:
#             return {"error": "clean_query failed", "detail": step1.text}
#         query_tokens = step1.json()["query_tokens"]

#         # 4. التمثيل (vectorization)
#         step2 = await client.post(SERVICES_URL["Vectorize_Embedding"], json={
#             "query_tokens": query_tokens,
#             "dataset_name": req.dataset_name,
#             "query_id": qid,
#             "raw_query": final_query
#         })
#         if step2.status_code != 200:
#             return {"error": "vectorization failed", "detail": step2.text}

#         # 5. الرتبة (Ranking)
#         ranking_url = SERVICES_URL["Ranking_FAISS"] if req.method.lower() == "faiss" else SERVICES_URL["Ranking"]
#         start = time.time()
#         if req.method.lower() == "faiss":
#             step3 = await client.post(ranking_url, params={
#                 "dataset": req.dataset_name,
#                 "query_id": qid,
#                 "top_k": 10
#             })
#         else:
#             step3 = await client.post(ranking_url, json={
#                 "representation": "embedding",
#                 "dataset": req.dataset_name,
#                 "query_id": qid,
#                 "top_k": 10
#             })
#         end = time.time()
#         print(f"⏱️ ranking_time : {end - start:.4f} s")

#         if step3.status_code != 200:
#             return {"error": "ranking failed", "detail": step3.text}

#         # 6. جلب نصوص المستندات المرتبة
#         doc_ids = [item["doc_id"] for item in step3.json().get("results", [])]
#         step4 = await client.post(SERVICES_URL["GET_DOCS_TEXTS"], json={
#             "dataset_name": req.dataset_name,
#             "doc_ids": doc_ids
#         })
#         if step4.status_code != 200:
#             return {"error": "get_docs_texts failed", "detail": step4.text}

#     return {
#         "texts": step4.json().get("texts", [])
#     }


from fastapi import FastAPI
from pydantic import BaseModel
import httpx
from utils.config import SERVICES_URL
from utils.middleware_cors_config import add_cors 
from utils.retrieval import get_next_qid
import time

app = FastAPI()
add_cors(app)

class QueryRequest(BaseModel):
    query: str
    dataset_name: str
    method: str = "default"
    chosen_option: str = "original"  # نستخدم القيمة من الواجهة

@app.post("/run_query_embedding")
async def run_query_embedding(req: QueryRequest):
    qid = get_next_qid()
    async with httpx.AsyncClient(timeout=30.0) as client:
         # لا ترسل مرة ثانية إلى /suggestions لأن الواجهة سبق وأرسلتها
        final_query = req.query

        step1 = await client.post(SERVICES_URL["LIGHT_CLEAN_QUERY"], json={"query": final_query})
        if step1.status_code != 200:
            return {"error": "clean_query failed", "detail": step1.text}
        query_tokens = step1.json()["query_tokens"]

        step2 = await client.post(SERVICES_URL["Vectorize_Embedding"], json={
            "query_tokens": query_tokens,
            "dataset_name": req.dataset_name,
            "query_id": qid,
            "raw_query": final_query
        })
        if step2.status_code != 200:
            return {"error": "vectorization failed", "detail": step2.text}

        ranking_url = SERVICES_URL["Ranking_FAISS"] if req.method.lower() == "faiss" else SERVICES_URL["Ranking"]
        start = time.time()
        if req.method.lower() == "faiss":
            step3 = await client.post(ranking_url, params={
                "dataset": req.dataset_name,
                "query_id": qid,
                "top_k": 10
            })
        else:
            step3 = await client.post(ranking_url, json={
                "representation": "embedding",
                "dataset": req.dataset_name,
                "query_id": qid,
                "top_k": 10
            })
        end = time.time()
        print(f"⏱️ ranking_time : {end - start:.4f} s")

        if step3.status_code != 200:
            return {"error": "ranking failed", "detail": step3.text}

        doc_ids = [item["doc_id"] for item in step3.json().get("results", [])]
        step4 = await client.post(SERVICES_URL["GET_DOCS_TEXTS"], json={
            "dataset_name": req.dataset_name,
            "doc_ids": doc_ids
        })
        if step4.status_code != 200:
            return {"error": "get_docs_texts failed", "detail": step4.text}

    return {
        "texts": step4.json().get("texts", [])
    }
