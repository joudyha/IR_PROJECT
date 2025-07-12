
import sqlite3
from utils.config import SQLITE_DB_PATH  # import مطلق

def create_tables_if_not_exist():
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS docs (
            doc_id TEXT,
            text TEXT,
            processed_text TEXT,
            dataset_name TEXT,
            PRIMARY KEY (doc_id, dataset_name)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS queries (
            query_id TEXT,
            text TEXT,
            dataset_name TEXT,
            PRIMARY KEY (query_id, dataset_name)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS qrels (
            query_id TEXT,
            doc_id TEXT,
            relevance INTEGER,
            dataset_name TEXT,
            PRIMARY KEY (query_id, doc_id, dataset_name)
        )
    ''')

    try:
        cursor.execute('ALTER TABLE docs ADD COLUMN light_clean_text TEXT')
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            pass
        else:
            raise

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables_if_not_exist()


