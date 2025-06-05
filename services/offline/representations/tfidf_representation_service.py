from fastapi import FastAPI, Query
from sklearn.feature_extraction.text import TfidfVectorizer
import sqlite3, joblib
import pandas as pd
from utils.config import SQLITE_DB_PATH

app = FastAPI()

@app.post("/build_tfidf")
def build_tfidf(dataset_name: str = Query(...)):
    conn = sqlite3.connect(SQLITE_DB_PATH)
    df = pd.read_sql("""
        SELECT doc_id, processed_text 
        FROM docs 
        WHERE dataset_name = ? AND processed_text IS NOT NULL
    """, conn, params=(dataset_name,))

    if df.empty:
        return {"error": f"No documents found for dataset '{dataset_name}'"}

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df["processed_text"])

    joblib.dump((vectorizer, X, df["doc_id"].tolist()), f"utils/joblib_files/tfidf_model/{dataset_name}_vectorizer.joblib")
    return {"status": "vectorizer saved", "documents": len(df)}
