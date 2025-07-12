
from fastapi import FastAPI, Query
import pandas as pd
import sqlite3
import os
from utils.config import SQLITE_DB_PATH
from utils.initialize import create_tables_if_not_exist
from utils.middleware_cors_config import add_cors

app = FastAPI()
add_cors(app)

@app.on_event("startup")
def init_db():
    create_tables_if_not_exist()
    print("✅ Database initialized and tables created.")

def fix_tabs_in_text(path):
    fixed_lines = []
    with open(path, 'r', encoding='utf-8') as f:
        header = f.readline()
        fixed_lines.append(header)
        for line in f:
            parts = line.rstrip('\n').split('\t')
            if len(parts) > 2:
                doc_id = parts[0]
                text = " ".join(parts[1:])
                fixed_line = f"{doc_id}\t{text}\n"
                fixed_lines.append(fixed_line)
            else:
                fixed_lines.append(line)
    fixed_path = path.replace(".tsv", "_fixed.tsv")
    with open(fixed_path, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    return fixed_path

@app.post("/load_raw_docs")
def load_raw_docs(dataset_name: str = Query(...)):
    try:
        path = f"datasets/{dataset_name}/docs.tsv"
        if not os.path.exists(path):
            return {"error": f"Dataset not found at path: {path}"}

        fixed_path = fix_tabs_in_text(path)

        df = pd.read_csv(fixed_path, sep="\t")

        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()

        inserted = 0
        for _, row in df.iterrows():
            cursor.execute(
                "INSERT OR IGNORE INTO docs (dataset_name, doc_id, text, processed_text, light_clean_text) VALUES (?, ?, ?, ?, ?)",
                (dataset_name, row["doc_id"], row["text"], None, None)
            )
            inserted += 1
    
        conn.commit()
        conn.close()

        os.remove(fixed_path)

        return {"loaded_docs": inserted}

    except Exception as e:
        import traceback; traceback.print_exc()
        return {"error": "Exception occurred", "details": str(e)}
