from fastapi import FastAPI, Query
from utils.config import SQLITE_DB_PATH
from rank_bm25 import BM25Okapi
from utils.clean_text import tokenize
import sqlite3, joblib, os
import pandas as pd

app = FastAPI()

@app.post("/build_BM25")
def build_bm25(dataset_name: str = Query(...), k1=1.5, b=0.75):
    with sqlite3.connect(SQLITE_DB_PATH) as conn:
        query = (
            "SELECT doc_id, processed_text "
            "FROM docs "
            "WHERE dataset_name = ? "
            "AND processed_text IS NOT NULL "
            "AND TRIM(processed_text) != ''"
        )
        df = pd.read_sql(query, conn, params=[dataset_name])

    if df.empty:
        return {"error": f"لا يوجد مستندات صالحة للمعالجة في المجموعة '{dataset_name}'"}

    tokenized_corpus = []
    valid_doc_ids = []

    for doc_id, text in zip(df["doc_id"], df["processed_text"]):
        tokens = tokenize(text)
        if tokens:  
            tokenized_corpus.append(tokens)
            valid_doc_ids.append(doc_id)

    if not tokenized_corpus:
        return {"error": "كل المستندات أصبحت فارغة بعد التوكنة. تحقق من التنظيف."}

    bm25_vectorizer = BM25Okapi(tokenized_corpus, k1=k1, b=b)

    representation = []
    for doc_tokens in tokenized_corpus:
        scores = bm25_vectorizer.get_scores(doc_tokens)
        representation.append(scores.tolist())

    output_dir = "utils/joblib_files/bm25_model"
    os.makedirs(output_dir, exist_ok=True)

    joblib.dump({
        "bm25_vectorizer": bm25_vectorizer,
        "doc_ids": valid_doc_ids,
        "bm25_matrix": representation,
        "tokenized_corpus": tokenized_corpus
    }, f"{output_dir}/{dataset_name}_bm25.joblib")

    return {
        "status": "BM25 model saved",
        "documents_loaded": len(df),
        "documents_tokenized": len(valid_doc_ids)
    }
