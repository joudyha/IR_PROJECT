# from fastapi import FastAPI, Query
# import pandas as pd
# import sqlite3
# import os
# from utils.config import SQLITE_DB_PATH
# from initialize import create_tables_if_not_exist
# app = FastAPI()

# @app.post("/load_raw_docs")
# def load_raw_docs(dataset_name: str = Query(...)):
#     create_tables_if_not_exist()

#     path = f"datasets/{dataset_name}/docs.tsv"
#     if not os.path.exists(path):
#         return {"error": "Dataset not found"}

#     df = pd.read_csv(path, sep="\t")
#     conn = sqlite3.connect(SQLITE_DB_PATH)
#     cursor = conn.cursor()

#     for _, row in df.iterrows():
#         cursor.execute(
#             "INSERT OR IGNORE INTO docs (dataset_name, doc_id, original_text, processed_text) VALUES (?, ?, ?, ?)",
#             (dataset_name, row["doc_id"], row["text"], None)
#         )
#         inserted += 1


#     conn.commit()
#     conn.close()
#     return {"loaded_docs": len(df)}

# services/offline/load_services.py

from fastapi import FastAPI, Query
import pandas as pd
import sqlite3
import os
from utils.config import SQLITE_DB_PATH
from initialize import create_tables_if_not_exist

app = FastAPI()

@app.on_event("startup")
def init_db():
   
    create_tables_if_not_exist()
    print("✅ Database initialized and tables created.")

@app.post("/load_raw_docs")
def load_raw_docs(dataset_name: str = Query(...)):
    try:
        # 1. تأكد من وجود المجلد والملف
        path = f"datasets/{dataset_name}/docs.tsv"
        if not os.path.exists(path):
            return {"error": f"Dataset not found at path: {path}"}

        # 2. اقرأ الملف إلى DataFrame
        df = pd.read_csv(path, sep="\t")
        print("Columns in TSV file:", df.columns.tolist())

        # 3. افتح اتصال SQLite
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()

        # 4. أدخل السجلات
        inserted = 0
        for _, row in df.iterrows():
            cursor.execute(
                "INSERT OR IGNORE INTO docs (dataset_name, doc_id,text, processed_text) VALUES (?, ?, ?, ?)",
                (dataset_name, row["doc_id"], row["text"], None)
            )
            inserted += 1

        conn.commit()
        conn.close()

        return {"loaded_docs": inserted}

    except Exception as e:
        # طباعة الخطأ تفصيليًّا في الكونسول
        import traceback; traceback.print_exc()
        # إعادة الخطأ جزئيًّا في الاستجابة لتصحيح سريع
        return {"error": "Exception occurred", "details": str(e)}
