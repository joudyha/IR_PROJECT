# from fastapi import FastAPI
# from pydantic import BaseModel
# import joblib, os
# import numpy as np
# from sentence_transformers import SentenceTransformer
# from typing import List
# from utils.middleware_cors_config import add_cors 

# app = FastAPI()
# add_cors(app)

# class CleanedQuery(BaseModel):
#     query_tokens: List[str]
#     dataset_name: str
#     query_id: str  # أضفنا هذا لحفظ ملف الاستعلام

# @app.post("/vectorize_hybrid")
# def vectorize_hybrid(cleaned: CleanedQuery):
#     # 1. Load hybrid model (to get the TF-IDF vectorizer)
#     hybrid_model_path = f"utils/joblib_files/hybrid_model/{cleaned.dataset_name}_hybrid.joblib"
#     if not os.path.exists(hybrid_model_path):
#         return {"error": f"Hybrid model not found for {cleaned.dataset_name}"}
    
#     hybrid_model = joblib.load(hybrid_model_path)
#     tfidf_vectorizer = hybrid_model["tfidf_vectorizer"]

#     # 2. Compute TF-IDF vector
#     tfidf_vec = tfidf_vectorizer.transform([" ".join(cleaned.query_tokens)]).toarray()

#     # 3. Compute BERT embedding
#     model = SentenceTransformer('D:/GRADUATE/IR_Project_LFE/utils/Bert_model/multi-qa-MiniLM-L6-cos-v1')
#     emb_vec = model.encode([" ".join(cleaned.query_tokens)])

#     # 4. Concatenate both vectors to form hybrid vector
#     hybrid_vec = np.hstack((tfidf_vec, emb_vec))

#     # 5. Save query vector
#     save_path = f"utils/joblib_files/query_vectors/{cleaned.dataset_name}_hybrid_{cleaned.query_id}.joblib"
#     os.makedirs(os.path.dirname(save_path), exist_ok=True)
#     joblib.dump({"query_vector": hybrid_vec}, save_path)

#     return {
#         "vector": hybrid_vec.tolist(),
#         "saved_to": save_path
#     }



# # @app.post("/vectorize_hybrid")
# # def vectorize_hybrid(query: HybridQuery):
# #     hybrid_model_path = f"utils/joblib_files/hybrid_model/{query.dataset_name}_hybrid.joblib"
# #     if not os.path.exists(hybrid_model_path):
# #         return {"error": f"Hybrid model not found for {query.dataset_name}"}
    
# #     hybrid_model = joblib.load(hybrid_model_path)
# #     tfidf_vectorizer = hybrid_model["tfidf_vectorizer"]

# #     # تحويل قائمة كلمات TF-IDF إلى نص (لـ vectorizer)
# #     tfidf_text = " ".join(query.heavy_tokens)

# #     # حساب متجه TF-IDF
# #     tfidf_vec = tfidf_vectorizer.transform([tfidf_text]).toarray()

# #     # حساب متجه embedding باستخدام النص الخفيف المنظف (embedding_text)
# #     emb_vec = model.encode([query.light_text])

# #     # دمج المتجهات
# #     hybrid_vec = np.hstack((tfidf_vec, emb_vec))

# #     # حفظ المتجه
# #     save_path = f"utils/joblib_files/query_vectors/{query.dataset_name}_hybrid_{query.query_id}.joblib"
# #     os.makedirs(os.path.dirname(save_path), exist_ok=True)
# #     joblib.dump({"query_vector": hybrid_vec}, save_path)

# #     return {
# #         "vector": hybrid_vec.tolist(),
# #         "saved_to": save_path
# #     }





from fastapi import FastAPI
from pydantic import BaseModel
import joblib, os
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List
from utils.middleware_cors_config import add_cors 
from sklearn.preprocessing import normalize

app = FastAPI()
add_cors(app)

bert_model_path = 'D:/GRADUATE/IR_Project_LFE/utils/Bert_model/all-MiniLM-L6-v2'
model = SentenceTransformer(bert_model_path)

class HybridQuery(BaseModel):
    heavy_tokens: List[str]
    light_tokens: List[str]
    light_text: str
    dataset_name: str
    query_id: str

@app.post("/vectorize_hybrid")
def vectorize_hybrid(query: HybridQuery, alpha: float = 0.5):
    hybrid_model_path = f"D:/GRADUATE/IR_Project_LFE/utils/joblib_files/hybrid_model/{query.dataset_name}_hybrid.joblib"
    if not os.path.exists(hybrid_model_path):
        return {"error": f"Hybrid model not found for {query.dataset_name}"}
    
    hybrid_model = joblib.load(hybrid_model_path)
    tfidf_vectorizer = hybrid_model["vectorizer"]

    tfidf_text = " ".join(query.heavy_tokens)
    tfidf_vec = tfidf_vectorizer.transform([tfidf_text]).toarray()
    emb_vec = model.encode([query.light_text])

    tfidf_vec = normalize(tfidf_vec)
    emb_vec = normalize(emb_vec)

    tfidf_weighted = alpha * tfidf_vec
    emb_weighted = (1 - alpha) * emb_vec

    hybrid_vec = np.hstack((tfidf_weighted, emb_weighted))

    save_path = f"D:/GRADUATE/IR_Project_LFE/utils/joblib_files/query_vectors/{query.dataset_name}_hybrid_{query.query_id}.joblib"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    joblib.dump({"query_vector": hybrid_vec}, save_path)

    return {
        "vector": hybrid_vec.tolist(),
        "saved_to": save_path,
        "alpha": alpha
    }
