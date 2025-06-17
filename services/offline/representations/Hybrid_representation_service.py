from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from utils.config import SQLITE_DB_PATH
from fastapi import FastAPI, Query
import sqlite3, joblib
import pandas as pd
import os
import numpy as np
from utils.middleware_cors_config import add_cors
from utils.clean_text import processing, tokenize
from utils.clean_text import clean_text

app = FastAPI()
add_cors(app)

@app.post("/build_hybrid")
def build_hybrid(dataset_name: str = Query(...)):
    conn = sqlite3.connect(SQLITE_DB_PATH)
    df = pd.read_sql("""
        SELECT doc_id, text 
        FROM docs 
        WHERE dataset_name = ? AND text IS NOT NULL
    """, conn, params=(dataset_name,))

    if df.empty:
        return {"error": f"No documents found for dataset '{dataset_name}'"}

  
    # ✅ TF-IDF
    tfidf_vectorizer = TfidfVectorizer(
        preprocessor=processing,
        tokenizer=tokenize,
        lowercase=False,
        token_pattern=None
    )
    tfidf_vectors = tfidf_vectorizer.fit_transform(df["text"]).toarray()
    print("Sample raw text:", df["text"].iloc[0])
    print("After clean_text:", clean_text(df["text"].iloc[0]))
    print("Joined:", " ".join(clean_text(df["text"].iloc[0])))
  
     # ✅ BERT باستخدام clean_text ثم join لإرجاع نصوص جاهزة
    cleaned_for_bert = [" ".join(clean_text(x)) for x in df["text"]]
    model = SentenceTransformer('all-MiniLM-L6-v2')
    bert_embeddings = model.encode(cleaned_for_bert, convert_to_numpy=True)

    print("TF-IDF shape:", tfidf_vectors.shape)
    print("BERT shape:", bert_embeddings.shape)

    # ✅ دمج
    hybrid_vectors = np.concatenate([tfidf_vectors, bert_embeddings], axis=1)
    os.makedirs("utils/joblib_files/hybrid_model", exist_ok=True)

    joblib.dump({
        "tfidf_vectorizer": tfidf_vectorizer,
        "hybrid_vectors": hybrid_vectors,
        "doc_ids": df["doc_id"].tolist()
    }, f"utils/joblib_files/hybrid_model/{dataset_name}_hybrid.joblib")

    return {"status": "Hybrid vectors saved", "documents": len(df)}
    