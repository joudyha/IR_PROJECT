
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

@app.post("/run_bm25_pipeline")
async def run_pipeline(req: DatasetRequest):
    ds = req.dataset_name
    # print("running step 1 ")

    async with httpx.AsyncClient(timeout=100000) as client:
        # step1 = await client.post(SERVICES_URL["LOAD_RAW_DOCS"], params={"dataset_name": ds}, timeout=60)
        # if step1.status_code != 200:
        #     return {"error": "loading failed", "detail": step1.text}
        # print("STEP 1 done")

        # print("running step 2 ")
        # step2 = await client.post(SERVICES_URL["CLEAN_STORED_DOCS"], params={"dataset_name": ds}, timeout=60)
        # if step2.status_code != 200:
        #     return {"error": "cleaning failed", "detail": step2.text}
        # print("STEP 2 done")

        print("running step 3 ")
        step3 = await client.post(SERVICES_URL["BUILD_BM25"], params={"dataset_name": ds}, timeout=100000)
        if step3.status_code != 200:
            return {"error": "bm25_representation failed", "detail": step3.text}
        print("STEP 3 done")

        print("running step 4 ")
        step4 = await client.post(SERVICES_URL["INVERTED_INDEX"], params={"dataset_name": ds}, timeout=100000)
        if step4.status_code != 200:
            return {"error": "inverted_index failed", "detail": step4.text}
        print("STEP 4 done")

    return {
        "status": "Pipeline completed",
        "details": {
            # "raw_load": step1.json(),
            # "cleanning": step2.json(),
            "bm25": step3.json(),
            "inverted_index": step4.json()
        }
    }
