import sqlite3
import pandas as pd
from fastapi import  FastAPI,Query
import gensim.downloader as api
from utils.config import SQLITE_DB_PATH
glove_vectors = api.load("glove-wiki-gigaword-100")


app=FastAPI()

@app.post('/topic_detection')
def topic_detection(dataset_name:str=Query(...)):
    conn = sqlite3.connect(SQLITE_DB_PATH)
    df = pd.read_sql("""
           SELECT doc_id, processed_text 
           FROM docs 
           WHERE dataset_name = ? AND processed_text IS NOT NULL
       """, conn, params=(dataset_name,))

    if df.empty:
        return {"error": f"No documents found for dataset '{dataset_name}'"}
