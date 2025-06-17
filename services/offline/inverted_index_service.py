from fastapi import FastAPI, Query
import sqlite3
from collections import defaultdict
import json
from utils.config import SQLITE_DB_PATH
import pandas as pd
import os
from utils.middleware_cors_config import add_cors 
app = FastAPI()
add_cors(app)
@app.post("/build_inverted_index")
def build_index(dataset_name: str = Query(...)):
    conn = sqlite3.connect(SQLITE_DB_PATH)
    
    # استرجاع البيانات الخاصة بالـ dataset فقط
    df = pd.read_sql("SELECT doc_id, processed_text FROM docs WHERE dataset_name = ?", conn, params=(dataset_name,))

    index = defaultdict(set)
    for _, row in df.iterrows():
        for word in row["processed_text"].split():
            index[word].add(row["doc_id"])

    index = {k: list(v) for k, v in index.items()}

    os.makedirs("utils/inverted_index", exist_ok=True)
    with open(f"utils/inverted_index/{dataset_name}_index.json", "w") as f:
        json.dump(index, f)

    return {"status": f"{dataset_name} index saved"}
