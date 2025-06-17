
# # import ir_datasets

# # dataset = ir_datasets.load("antique")
# # for doc in dataset.docs_iter():
# #     print(doc.doc_id,doc.text)
# # # dataset = ir_datasets.load("lotte/lifestyle/dev/forum")
# # # # import ir_datasets

# # # dataset=ir_datasets.load("antique/train")
# # # print(dataset)

# # # # # for doc in dataset.docs_iter():
# # # # #     print(doc.doc_id,doc.text)
    

# # # # import ir_datasets

# # # # dataset = ir_datasets.load("lotte/lifestyle/dev/forum")
# # # # corpus = {doc.doc_id: doc.text for doc in dataset.docs_iter() if isinstance(doc.text, str)}
# # # # print(corpus)

# # # # # try:
# # # # #     for query in dataset.queries_iter():
# # # # #         pass
# # # # # except AttributeError:
# # # # #     print("No queries in this dataset")

# # # # # # لتحميل ال qrels لو موجودة
# # # # # try:
# # # # #     for qrel in dataset.qrels_iter():
# # # # #         pass
# # # # # except AttributeError:
# # # # #     print("No qrels in this dataset")

# # # # # print(dataset.docs_path())
# # # # # print(dataset.queries_path())
# # # # # print(dataset.qrels_path())



# # # # import ir_datasets
# # # import csv
# # # import os

# # # # # تحديد اسم الداتاست والقسم (train/test)
# # # DATASET_NAME = "antique/train"

# # # # # المجلد اللي بدك تحفظ فيه الملفات
# # # SAVE_DIR = "antique_train_data"
# # # os.makedirs(SAVE_DIR, exist_ok=True)

# # # # تحميل الداتاست
# # # dataset = ir_datasets.load(DATASET_NAME)

# # # # 1. حفظ المستندات (docs)
# # # docs_file = os.path.join(SAVE_DIR, "docs.tsv")
# # # with open(docs_file, "w", encoding="utf-8", newline='') as f:
# # #     writer = csv.writer(f, delimiter='\t')
# # #     writer.writerow(["doc_id", "text"])
# # #     for doc in dataset.docs_iter():
# # #         writer.writerow([doc.doc_id, doc.text])
# # # print(f"Saved docs to {docs_file}")

# # # # #2. حفظ الاستعلامات (queries)
# # # # queries_file = os.path.join(SAVE_DIR, "queries.tsv")
# # # # with open(queries_file, "w", encoding="utf-8", newline='') as f:
# # # #     writer = csv.writer(f, delimiter='\t')
# # # #     writer.writerow(["query_id", "text"])
# # # #     for query in dataset.queries_iter():
# # # #         writer.writerow([query.query_id, query.text])
# # # # print(f"Saved queries to {queries_file}")

# # # # 3. حفظ الـ qrels (العلاقات بين queries والمستندات)
# # # qrels_file = os.path.join(SAVE_DIR, "qrels.tsv")
# # # with open(qrels_file, "w", encoding="utf-8", newline='') as f:
# # #     writer = csv.writer(f, delimiter='\t')
# # #     writer.writerow(["query_id", "doc_id", "relevance"])
# # #     for qrel in dataset.qrels_iter():
# # #         writer.writerow([qrel.query_id, qrel.doc_id, qrel.relevance])
# # # print(f"Saved qrels to {qrels_file}")
# import os
# import csv
# import sqlite3
# from utils.config import DATA_PATH
# def create_tables(cursor):
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS docs (
#             doc_id TEXT,
#             text TEXT,
#             dataset_name TEXT,
#             PRIMARY KEY (doc_id, dataset_name)
#         )
#     ''')
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS queries (
#             query_id TEXT,
#             text TEXT,
#             dataset_name TEXT,
#             PRIMARY KEY (query_id, dataset_name)
#         )
#     ''')
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS qrels (
#             query_id TEXT,
#             doc_id TEXT,
#             relevance INTEGER,
#             dataset_name TEXT,
#             PRIMARY KEY (query_id, doc_id, dataset_name)
#         )
#     ''')
#     conn = sqlite3.connect(DATA_PATH)
#     cursor = conn.cursor()
#     create_tables(cursor)


# # def load_tsv_to_db(file_path, table, columns, dataset_name, cursor):
# #     with open(file_path, encoding='utf-8') as f:
# #         reader = csv.reader(f, delimiter='\t')
# #         for row in reader:
# #             row = list(row) + [dataset_name]
# #             placeholders = ','.join(['?'] * len(row))
# #             cursor.execute(f'INSERT OR IGNORE INTO {table} VALUES ({placeholders})', row)

# # def import_dataset(dataset_path, dataset_name, db_path='datasets.db'):
# #     if not os.path.isdir(dataset_path):
# #         raise FileNotFoundError(f"Directory {dataset_path} not found.")

  
# #     print(f"📥 Importing dataset '{dataset_name}'...")

# #     load_tsv_to_db(os.path.join(dataset_path, 'docs.tsv'), 'docs', ['doc_id', 'text'], dataset_name, cursor)
# #     load_tsv_to_db(os.path.join(dataset_path, 'queries.tsv'), 'queries', ['query_id', 'text'], dataset_name, cursor)
# #     load_tsv_to_db(os.path.join(dataset_path, 'qrels.tsv'), 'qrels', ['query_id', 'doc_id', 'relevance'], dataset_name, cursor)

# #     conn.commit()
# #     conn.close()
# #     print(f"✅ Dataset '{dataset_name}' imported successfully.\n")

# # # === الاستخدام ===
# # import_dataset('antique_train_data', 'antique')
# # import_dataset('lotte_train_data', 'lotte')
import sqlite3
from utils.config import SQLITE_DB_PATH
def create_tables_if_not_exist():
    
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()

    # إنشاء جدول المستندات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS docs (
            doc_id TEXT,
            text TEXT,
            processed_text TEXT,
            dataset_name TEXT,
            PRIMARY KEY (doc_id, dataset_name)
        )
    ''')

    # إنشاء جدول الاستعلامات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS queries (
            query_id TEXT,
            text TEXT,
            dataset_name TEXT,
            PRIMARY KEY (query_id, dataset_name)
        )
    ''')

    # إنشاء جدول الارتباط بين الاستعلام والمستند
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS qrels (
            query_id TEXT,
            doc_id TEXT,
            relevance INTEGER,
            dataset_name TEXT,
            PRIMARY KEY (query_id, doc_id, dataset_name)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables_if_not_exist()