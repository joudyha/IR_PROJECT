from sklearn.preprocessing import normalize
from sklearn.decomposition import TruncatedSVD
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
from utils.clean_text import clean_text,light_clean

app = FastAPI()
add_cors(app)

@app.post("/build_hybrid")
def build_hybrid(dataset_name: str = Query(...), use_svd: bool = False, svd_dim: int = 300):
    tfidf_path = f"D:/GRADUATE/IR_Project_LFE/utils/joblib_files/tfidf_model/{dataset_name}_tfidf.joblib"
    bert_path = f"D:/GRADUATE/IR_Project_LFE/utils/joblib_files/embedding_model/{dataset_name}_embedding.joblib"
    
    if not os.path.exists(tfidf_path):
        return {"error": f"TF-IDF file not found for dataset '{dataset_name}'"}
    if not os.path.exists(bert_path):
        return {"error": f"BERT file not found for dataset '{dataset_name}'"}
    
    tfidf_data = joblib.load(tfidf_path)
    bert_data = joblib.load(bert_path)
    
    if tfidf_data["doc_ids"] != bert_data["doc_ids"]:
        return {"error": "Mismatch in doc_ids between TF-IDF and BERT files"}

    tfidf_vectors = normalize(tfidf_data["tfidf_vectors"])
    bert_vectors = normalize(bert_data["bert_embeddings"])

    if use_svd:
        svd = TruncatedSVD(n_components=svd_dim, random_state=42)
        tfidf_vectors = svd.fit_transform(tfidf_vectors)

    hybrid_vectors = np.concatenate([tfidf_vectors, bert_vectors], axis=1)

    hybrid_path = f"utils/joblib_files/hybrid_model/{dataset_name}_hybrid.joblib"
    os.makedirs("utils/joblib_files/hybrid_model", exist_ok=True)
    joblib.dump({
        "tfidf_vectorizer": tfidf_data["tfidf_vectorizer"],
        "hybrid_vectors": hybrid_vectors,
        "doc_ids": tfidf_data["doc_ids"]
    }, hybrid_path)

    return {
        "status": "Hybrid vectors merged and saved",
        "doc_count": len(tfidf_data["doc_ids"]),
        "hybrid_shape": hybrid_vectors.shape
    }
  

















    # return {
    #     "status": "Hybrid vectors merged and saved",
    #     "doc_count": len(tfidf_data["doc_ids"]),
    #     "hybrid_shape": hybrid_vectors.shape
    # }
# from sklearn.preprocessing import normalize
# from sklearn.decomposition import TruncatedSVD
# from fastapi import FastAPI, Query
# import os, joblib
# import numpy as np
# from utils.middleware_cors_config import add_cors

# app = FastAPI()
# add_cors(app)

# @app.post("/build_hybrid")
# def build_hybrid(dataset_name: str = Query(...), use_svd: bool = False, svd_dim: int = 300):
#     tfidf_path = f"D:/GRADUATE/IR_Project_LFE/utils/joblib_files/tfidf_model/{dataset_name}_tfidf.joblib"
#     bert_path = f"D:/GRADUATE/IR_Project_LFE/utils/joblib_files/embedding_model/{dataset_name}_embedding.joblib"

#     if not os.path.exists(tfidf_path):
#         return {"error": f"TF-IDF file not found for dataset '{dataset_name}'"}
#     if not os.path.exists(bert_path):
#         return {"error": f"BERT file not found for dataset '{dataset_name}'"}

#     tfidf_data = joblib.load(tfidf_path)
#     bert_data = joblib.load(bert_path)

#     tfidf_ids = tfidf_data["doc_ids"]
#     bert_ids = bert_data["doc_ids"]

#     tfidf_id_set = set(tfidf_ids)
#     bert_id_set = set(bert_ids)

#     common_ids = list(tfidf_id_set & bert_id_set)
#     missing_in_tfidf = list(bert_id_set - tfidf_id_set)
#     missing_in_bert = list(tfidf_id_set - bert_id_set)

#     if not common_ids:
#         return {"error": "No common doc_ids between TF-IDF and BERT files"}

#     if missing_in_tfidf or missing_in_bert:
#         print("❗ Mismatch Detected:")
#         if missing_in_tfidf:
#             print("Missing in TF-IDF:", missing_in_tfidf)
#         if missing_in_bert:
#             print("Missing in BERT:", missing_in_bert)

#     # بناء قاموس يربط ID بالمؤشر
#     tfidf_idx_map = {doc_id: idx for idx, doc_id in enumerate(tfidf_ids)}
#     bert_idx_map = {doc_id: idx for idx, doc_id in enumerate(bert_ids)}

#     tfidf_vectors = normalize(tfidf_data["vectors"])
#     bert_vectors = normalize(bert_data["embeddings"])

#     # استخراج فقط المشترك
#     safe_common_ids = [
#     doc_id for doc_id in common_ids
#     if doc_id in tfidf_idx_map and doc_id in bert_idx_map
#     ]

#     tfidf_common = np.array([tfidf_vectors[tfidf_idx_map[doc_id]] for doc_id in safe_common_ids])
#     bert_common = np.array([bert_vectors[bert_idx_map[doc_id]] for doc_id in safe_common_ids])
#     print("شكل tfidf_common:", tfidf_common.shape)
#     print("شكل bert_common:", bert_common.shape)

#     # تقليل الأبعاد إن لزم
#     if use_svd:
#         svd = TruncatedSVD(n_components=svd_dim, random_state=42)
#         tfidf_common = svd.fit_transform(tfidf_common)

#     hybrid_vectors = np.concatenate([tfidf_common, bert_common], axis=1)

#     # حفظ النموذج
#     hybrid_path = f"utils/joblib_files/hybrid_model/{dataset_name}_hybrid.joblib"
#     os.makedirs("utils/joblib_files/hybrid_model", exist_ok=True)
#     joblib.dump({
#         "tfidf_vectorizer": tfidf_data["tfidf_vectorizer"],
#         "hybrid_vectors": hybrid_vectors,
#         "doc_ids": safe_common_ids
#     }, hybrid_path)

#     return {
#         "status": "✅ Hybrid vectors merged and saved",
#         "doc_count": len(common_ids),
#         "excluded_in_tfidf": len(missing_in_tfidf),
#         "excluded_in_bert": len(missing_in_bert),
#         "hybrid_shape": hybrid_vectors.shape
#     }


# from sklearn.preprocessing import normalize
# from sklearn.decomposition import TruncatedSVD
# from fastapi import FastAPI, Query
# import os, joblib
# import numpy as np
# from utils.middleware_cors_config import add_cors

# app = FastAPI()
# add_cors(app)

# @app.post("/build_hybrid")
# def build_hybrid(dataset_name: str = Query(...), use_svd: bool = False, svd_dim: int = 300):
#     tfidf_path = f"D:/GRADUATE/IR_Project_LFE/utils/joblib_files/tfidf_model/{dataset_name}_tfidf.joblib"
#     bert_path = f"D:/GRADUATE/IR_Project_LFE/utils/joblib_files/embedding_model/{dataset_name}_embedding.joblib"

#     if not os.path.exists(tfidf_path):
#         return {"error": f"TF-IDF file not found for dataset '{dataset_name}'"}
#     if not os.path.exists(bert_path):
#         return {"error": f"BERT file not found for dataset '{dataset_name}'"}

#     tfidf_data = joblib.load(tfidf_path)
#     bert_data = joblib.load(bert_path)

#     tfidf_ids = tfidf_data["doc_ids"]
#     bert_ids = bert_data["doc_ids"]

#     tfidf_id_set = set(tfidf_ids)
#     bert_id_set = set(bert_ids)

#     common_ids = list(tfidf_id_set & bert_id_set)
#     missing_in_tfidf = list(bert_id_set - tfidf_id_set)
#     missing_in_bert = list(tfidf_id_set - bert_id_set)

#     if not common_ids:
#         return {"error": "No common doc_ids between TF-IDF and BERT files"}

#     if missing_in_tfidf or missing_in_bert:
#         print("❗ Mismatch Detected:")
#         if missing_in_tfidf:
#             print("Missing in TF-IDF:", missing_in_tfidf)
#         if missing_in_bert:
#             print("Missing in BERT:", missing_in_bert)

#     tfidf_idx_map = {doc_id: idx for idx, doc_id in enumerate(tfidf_ids)}
#     bert_idx_map = {doc_id: idx for idx, doc_id in enumerate(bert_ids)}

#     tfidf_vectors = normalize(tfidf_data["vectors"])
#     bert_vectors = normalize(bert_data["embeddings"])

#     safe_common_ids = [
#         doc_id for doc_id in common_ids
#         if doc_id in tfidf_idx_map and doc_id in bert_idx_map
#     ]

#     tfidf_common = np.array([tfidf_vectors[tfidf_idx_map[doc_id]] for doc_id in safe_common_ids])
#     bert_common = np.array([bert_vectors[bert_idx_map[doc_id]] for doc_id in safe_common_ids])

#     print("شكل tfidf_common:", tfidf_common.shape)
#     print("شكل bert_common:", bert_common.shape)

#     if use_svd:
#         svd = TruncatedSVD(n_components=svd_dim, random_state=42)
#         tfidf_common = svd.fit_transform(tfidf_common)

#     # تأكد أن tfidf_common مصفوفة 2D قبل الدمج
#     if tfidf_common.ndim == 1:
#         tfidf_common = tfidf_common[:, None]  # تحويلها لشكل (N,1)

#     hybrid_vectors = np.concatenate([tfidf_common, bert_common], axis=1)

#     hybrid_path = f"utils/joblib_files/hybrid_model/{dataset_name}_hybrid.joblib"
#     os.makedirs("utils/joblib_files/hybrid_model", exist_ok=True)
#     joblib.dump({
#         "tfidf_vectorizer": tfidf_data["vectorizer"],
#         "hybrid_vectors": hybrid_vectors,
#         "doc_ids": safe_common_ids
#     }, hybrid_path)

#     return {
#         "status": "✅ Hybrid vectors merged and saved",
#         "doc_count": len(common_ids),
#         "excluded_in_tfidf": len(missing_in_tfidf),
#         "excluded_in_bert": len(missing_in_bert),
#         "hybrid_shape": hybrid_vectors.shape
#     }
# Save hybrid result
