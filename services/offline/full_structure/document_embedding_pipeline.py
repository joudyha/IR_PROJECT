
# from fastapi import FastAPI
# from pydantic import BaseModel
# import requests
# import httpx
# from utils.config import SERVICES_URL
# from utils.middleware_cors_config import add_cors 


# app = FastAPI()
# add_cors(app)


# class DatasetRequest(BaseModel):
#     dataset_name: str
#     method: str = "default"  # default or faiss

# @app.post("/run_embedding_pipeline")
# async def run_pipeline(req: DatasetRequest):

#     ds = req.dataset_name
#     method = req.method.lower()
#     print(f"running pipeline with method: {method}")

#     # print("running step 1 ")

#     async with httpx.AsyncClient(timeout=10000) as client:
#         step1 = await client.post(SERVICES_URL["LOAD_RAW_DOCS"], params={"dataset_name": ds}, timeout=100)
#         if step1.status_code != 200:
#             return {"error": "loading failed", "detail": step1.text}
#         print("STEP 1 done")

#         print("running step 2 ")
#         step2 = await client.post(SERVICES_URL["CLEAN_STORED_DOCS"], params={"dataset_name": ds}, timeout=1000)
#         if step2.status_code != 200:
#             return {"error": "cleaning failed", "detail": step2.text}
#         print("STEP 2 done")

#         print("running step 3 ")
#         step3 = await client.post(SERVICES_URL["BUILD_EMBEDDING"], params={"dataset_name": ds}, timeout=10000)
#         if step3.status_code != 200:
#             return {"error": "embedding_representation failed", "detail": step3.text}
#         print("STEP 3 done")



#         if method == "faiss":
#            print("running step 4 ")
#            step4 = await client.post(SERVICES_URL["BUILD_INDEX_FAISS"], params={"dataset_name": ds}, timeout=10000)
#            if step4.status_code != 200:
#               return {"error": "faiss_index_build failed", "detail": step4.text}
#            print("STEP faiss index done") 
    

#     return {
#         "status": "Pipeline completed",
#         "details": {
#             "raw_load": step1.json(),
#             "cleanning": step2.json(),
#             "embedding": step3.json(),
#             "faiss_index": step4.json()
#         }
#     }

from fastapi import FastAPI
from pydantic import BaseModel
import httpx
from utils.config import SERVICES_URL
from utils.middleware_cors_config import add_cors 


app = FastAPI()
add_cors(app)


class DatasetRequest(BaseModel):
    dataset_name: str
    method: str = "default"  # default or faiss


@app.post("/run_embedding_pipeline")
async def run_pipeline(req: DatasetRequest):

    ds = req.dataset_name
    method = req.method.lower()
    print(f"running pipeline with method: {method}")

    async with httpx.AsyncClient(timeout=10000) as client:
        # print("running step 3 ")
        # step3 = await client.post(SERVICES_URL["BUILD_EMBEDDING"], params={"dataset_name": ds}, timeout=10000)
        # if step3.status_code != 200:
        #     return {"error": "embedding_representation failed", "detail": step3.text}
        # print("STEP 3 done")

        # step1 = await client.post(SERVICES_URL["LOAD_RAW_DOCS"], params={"dataset_name": ds}, timeout=10000)
        # if step1.status_code != 200:
        #     return {"error": "loading failed", "detail": step1.text}
        # print("STEP 1 done")

        # print("running step 2 ")
        # step2 = await client.post(SERVICES_URL["CLEAN_STORED_DOCS"], params={"dataset_name": ds}, timeout=1000)
        # if step2.status_code != 200:
        #     return {"error": "cleaning failed", "detail": step2.text}
        # print("STEP 2 done")

  
        # متغير يحتوي على تفاصيل الخطوات
        details = {
            # "raw_load": step1.json(),
            # "cleanning": step2.json(),
            # "embedding": step3.json(),
        }

        if method == "faiss":
            print("running step 4 ")
            step4 = await client.post(SERVICES_URL["BUILD_INDEX_FAISS"], params={"dataset_name": ds}, timeout=10000)
            if step4.status_code != 200:
                return {"error": "faiss_index_build failed", "detail": step4.text}
            print("STEP faiss index done")
            details["faiss_index"] = step4.json()

    return {
        "status": "Pipeline completed",
        "details": details
    }
