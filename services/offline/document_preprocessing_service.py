from fastapi import FastAPI, Query
import sqlite3
from utils.clean_text import clean_text
from utils.config import SQLITE_DB_PATH,BATCH_SIZE
from utils.middleware_cors_config import add_cors 
app = FastAPI()
add_cors(app)

@app.post("/clean_stored_docs")
def clean_stored_docs(dataset_name: str = Query(...)):
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    total_updated = 0

    while True:
        # 1. اختر دفعة جديدة من المستندات غير المنظفة
        cursor.execute("""
            SELECT doc_id,text FROM docs 
            WHERE dataset_name = ? AND (processed_text IS NULL OR processed_text = '')
            LIMIT ?
        """, (dataset_name, BATCH_SIZE))
        rows = cursor.fetchall()

        if not rows:
            break  # لا يوجد المزيد

        # 2. نظف وأحدث المستندات
        for doc_id, text in rows:
            cleaned = " ".join(clean_text(text))
            cursor.execute(
                "UPDATE docs SET processed_text = ? WHERE doc_id = ? AND dataset_name = ?",
                (cleaned, doc_id, dataset_name)
            )
            total_updated += 1

        # 3. احفظ التغييرات في كل دفعة
        conn.commit()

    conn.close()
    return {"cleaned_docs": total_updated}
