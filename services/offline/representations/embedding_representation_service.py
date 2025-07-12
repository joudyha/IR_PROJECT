
from sentence_transformers import SentenceTransformer
from utils.config import SQLITE_DB_PATH
from fastapi import FastAPI, Query
import sqlite3, joblib
import pandas as pd
import  os
from utils.middleware_cors_config import add_cors 

app = FastAPI()
add_cors(app)

bert_model_path = 'D:/GRADUATE/IR_Project_LFE/utils/Bert_model/all-MiniLM-L6-v2'
model = SentenceTransformer(bert_model_path)


@app.post("/build_embedding")
def build_embedding(dataset_name: str = Query(...)):
    conn = sqlite3.connect(SQLITE_DB_PATH)
    df = pd.read_sql("""
        SELECT doc_id, light_clean_text,text
        FROM docs 
        WHERE dataset_name = ? AND light_clean_text IS NOT NULL
    """, conn, params=(dataset_name,))

    if df.empty:
        return {"error": f"No documents found for dataset '{dataset_name}'"}

    embeddings = model.encode(df["light_clean_text"], convert_to_numpy=True, normalize_embeddings=True)

    os.makedirs("utils/joblib_files/embedding_model", exist_ok=True)

    raw_docs = dict(zip(df["doc_id"], df["text"]))

    joblib.dump({
        "embeddings": embeddings,
        "doc_ids": df["doc_id"].tolist(),
        "raw_docs":raw_docs
    }, f"utils/joblib_files/embedding_model/{dataset_name}_embedding.joblib")

    return {"status": "BERT embeddings saved", "documents": len(df)}
