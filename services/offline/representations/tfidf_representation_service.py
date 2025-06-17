from fastapi import FastAPI, Query
from sklearn.feature_extraction.text import TfidfVectorizer
import sqlite3, joblib
import pandas as pd
import os
from utils.config import SQLITE_DB_PATH
from utils.clean_text import processing,tokenize
from utils.middleware_cors_config import add_cors 

app = FastAPI()
add_cors(app)

@app.post("/build_tfidf")
def build_tfidf(dataset_name: str = Query(...)):
    conn = sqlite3.connect(SQLITE_DB_PATH)
    df = pd.read_sql("""
        SELECT doc_id, text 
        FROM docs 
        WHERE dataset_name = ? AND text IS NOT NULL
    """, conn, params=(dataset_name,))

    if df.empty:
        return {"error": f"No documents found for dataset '{dataset_name}'"}

    # ✅ نظف النصوص الخام باستخدام تابعك
    vectorizer = TfidfVectorizer(
    preprocessor=processing,
    tokenizer=tokenize,
    lowercase=False,
    token_pattern=None
)

    X = vectorizer.fit_transform(df["text"])

    os.makedirs("utils/joblib_files/tfidf_model", exist_ok=True)

    joblib.dump({
        "vectorizer": vectorizer,
        "vectors": X,
        "doc_ids": df["doc_id"].tolist()
    }, f"utils/joblib_files/tfidf_model/{dataset_name}_tfidf.joblib")

    return {"status": "TF-IDF saved", "documents": len(df)}