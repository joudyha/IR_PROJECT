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

# @app.post("/run_hybrid_pipeline")
# async def run_pipeline(req: DatasetRequest):
#     ds = req.dataset_name
#     print("running step 1 ")
#     async with httpx.AsyncClient() as client:
#         step1 = requests.post(SERVICES_URL["LOAD_RAW_DOCS"], params={"dataset_name": ds}, timeout=10)
#         if step1.status_code != 200:
#          return {"error": "loading failed", "detail": step1.text}
#         print("STEP 1 done")
    
#     print("running step 2 ")
#     async with httpx.AsyncClient() as client:
#       step2 = requests.post(SERVICES_URL["CLEAN_STORED_DOCS"], params={"dataset_name": ds}, timeout=10)
#       if step2.status_code != 200:
#         return {"error": "cleaning failed", "detail": step2.text}
#     print("STEP 2 done")
#     print("running step 3 ")
#     async with httpx.AsyncClient() as client:
#       step3 = requests.post(SERVICES_URL["BUILD_HYBRID"], params={"dataset_name": ds}, timeout=20)
#       if step3.status_code != 200:
#         return {"error": "hyprid_representation failed", "detail": step3.text}
#     print("STEP 3 done")

#     # # step4: test TF-IDF representation on a dummy sentence
#     # step4_data = {
#     #     "representation_type": "tfidf",
#     #     "text": "chees contain lot fat tasti treat cat realli treat think probabl want reduc quantiti bit mayb fifth make special snack instead look altern treat hard treat keep teeth good shape",
#     #     "dataset_name": ds
#     # }
#     # step4 = requests.post("http://localhost:8005/represent_text", json=step4_data)
#     # if step4.status_code != 200:
#     #     return {"error": "tfidf_representation failed", "detail": step4.text}
   
#     # print("running step 4 ")
#     # async with httpx.AsyncClient() as client:
#     #   step4 = requests.post(SERVICES_URL["INVERTED_INDEX"], params={"dataset_name": ds}, timeout=10)
#     #   if step4.status_code != 200:
#     #     return {"error": "inverted_index failed", "detail": step4.text}
#     # print("STEP 4 done")

#     return {
#         "status": "Pipeline completed",
#         "details": {
#             "raw_load": step1.json(),
#             "cleaning": step2.json(),
#             "hybrid": step3.json(),
#             # "representation_sample": step4.json(),
#             # "inverted_index": step4.json()
#         }
#     }



from fastapi import FastAPI
from pydantic import BaseModel
import requests
import httpx
from utils.config import SERVICES_URL
from utils.middleware_cors_config import add_cors 


app = FastAPI()
add_cors(app)


class DatasetRequest(BaseModel):
    dataset_name: str

@app.post("/run_hybrid_pipeline")
async def run_pipeline(req: DatasetRequest):
    ds = req.dataset_name
    print("running step 1 ")

    async with httpx.AsyncClient(timeout=30.0) as client:
        step1 = await client.post(SERVICES_URL["LOAD_RAW_DOCS"], params={"dataset_name": ds}, timeout=10)
        if step1.status_code != 200:
            return {"error": "loading failed", "detail": step1.text}
        print("STEP 1 done")

        # print("running step 2 ")
        # step2 = await client.post(SERVICES_URL["CLEAN_STORED_DOCS"], params={"dataset_name": ds}, timeout=10)
        # if step2.status_code != 200:
        #     return {"error": "cleaning failed", "detail": step2.text}
        # print("STEP 2 done")

        print("running step 2 ")
        step2 = await client.post(SERVICES_URL["BUILD_HYBRID"], params={"dataset_name": ds}, timeout=30)
        if step2.status_code != 200:
            return {"error": "hybrid_representation failed", "detail": step2.text}
        print("STEP 2 done")

        # print("running step 3 ")
        # step3 = await client.post(SERVICES_URL["INVERTED_INDEX"], params={"dataset_name": ds}, timeout=10)
        # if step3.status_code != 200:
        #     return {"error": "inverted_index failed", "detail": step3.text}
        # print("STEP 3 done")

    return {
        "status": "Pipeline completed",
        "details": {
            "raw_load": step1.json(),
            "hybrid": step2.json(),
            # "hybrid": step3.json(),
            # "inverted_index": step3.json()
        }
    }
