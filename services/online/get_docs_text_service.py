from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from utils.config import SQLITE_DB_PATH
from utils.middleware_cors_config import add_cors

app = FastAPI()
add_cors(app)

class DocsRequest(BaseModel):
    dataset_name: str
    doc_ids: list[str]
    
@app.post("/get_docs_texts")
def get_docs_texts(req: DocsRequest):
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()

    placeholders = ",".join("?" for _ in req.doc_ids)
    query = f"""
        SELECT doc_id, text
        FROM docs
        WHERE dataset_name = ? AND doc_id IN ({placeholders}) AND text IS NOT NULL
    """

    params = [req.dataset_name] + req.doc_ids
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    # 🧠 تحويل النتائج إلى dict: {doc_id: text}
    doc_map = {doc_id: text for doc_id, text in rows}

    # ✅ ترتيب حسب ترتيب doc_ids الأصلي
    texts = [
        {"doc_id": doc_id, "text": doc_map[doc_id]}
        for doc_id in req.doc_ids if doc_id in doc_map
    ]

    return {"texts": texts}
