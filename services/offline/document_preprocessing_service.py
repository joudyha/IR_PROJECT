from fastapi import FastAPI, Query
import sqlite3
from utils.clean_text import clean_text,light_clean
from utils.config import SQLITE_DB_PATH,BATCH_SIZE
from utils.middleware_cors_config import add_cors 
app = FastAPI()
add_cors(app)

@app.post("/clean_stored_docs")
def clean_stored_docs(dataset_name: str = Query(...)):
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    total_updated = 0
    batch_number = 0

    while True:
        cursor.execute("""
            SELECT doc_id, text FROM docs 
            WHERE dataset_name = ? AND (processed_text IS NULL OR processed_text = '')
            LIMIT ?
        """, (dataset_name, BATCH_SIZE))
        rows = cursor.fetchall()

        if not rows:
            break

        batch_number += 1
        print(f"[Batch {batch_number}] Cleaning {len(rows)} documents...", flush=True)

        for doc_id, text in rows:
            heavy_cleaned = " ".join(clean_text(text))  
            
            light_cleaned = light_clean(text)           
            cursor.execute("""
                UPDATE docs
                SET processed_text = ?, light_clean_text = ?
                WHERE doc_id = ? AND dataset_name = ?
            """, (heavy_cleaned, light_cleaned, doc_id, dataset_name))

            total_updated += 1

        conn.commit()

    conn.close()
    return {"cleaned_docs": total_updated}
