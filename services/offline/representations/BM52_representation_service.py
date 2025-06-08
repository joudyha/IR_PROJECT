from fastapi import FastAPI, Query
from utils.config import SQLITE_DB_PATH
from rank_bm25 import BM25Okapi
import sqlite3, joblib
import threading
import os
import pandas as pd

app = FastAPI()


@app.post("/build_BM25")
def build_bm25(dataset_name: str = Query(...),k1=1.5, b=0.75):
    conn = sqlite3.connect(SQLITE_DB_PATH)
    query = (
        "SELECT doc_id, processed_text "
        "FROM docs "
        "WHERE dataset_name = ? AND processed_text IS NOT NULL"
    )
    df = pd.read_sql(query, conn, params=[dataset_name])

    if df.empty:
        return {"error": f"No documents found for dataset '{dataset_name}'"}
    tokenized_corpus = (doc.split() for doc in df['processed_text'])
    bm25_vectorizer = BM25Okapi(df['processed_text'], k1=k1, b=b)
    representation = []
    for doc_index, doc in enumerate(tokenized_corpus):
        doc_scores = []
        for term in doc:
            term_scores = bm25_vectorizer.get_scores([term])
            doc_scores.append(term_scores[doc_index])  # Get score for current document only
        representation.append(doc_scores)

    output_dir = f"utils/joblib_files/bm25_model"
    os.makedirs(output_dir, exist_ok=True)
    joblib.dump((bm25_vectorizer, df["doc_id"].tolist(), representation),
                    f"utils/joblib_files/bm25_model/{dataset_name}_vectorizer.joblib")

    return {"status": "vectorizer saved", "documents": len(df)}

# def run_thread(dataset_name: str = Query(...),k1=1.5, b=0.75):
#     thread = threading.Thread(target=build_bm25, args=(dataset_name,k1,b))
#     thread.start()
#     return {"status": "Thread started for BM25 building."}