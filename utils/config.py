#=====SQLITE_DB=====#
SQLITE_DB_PATH="datasets.db"


#=====SERVICES_URL=====#

SERVICES_URL={

    #====OFFLINE_SERVICES=====#
    "LOAD_RAW_DOCS":"http://localhost:8001/load_raw_docs",
    "CLEAN_STORED_DOCS":"http://localhost:8004/clean_stored_docs",
    "BUILD_TFIDF":"http://localhost:8002/build_tfidf",
    "INVERTED_INDEX":"http://localhost:8003/build_inverted_index",
    "BUILD_HYBRID":"http://localhost:8005/build_hybrid",
    "BUILD_EMBEDDING":"http://localhost:8006/build_embedding",
    "BUILD_BM25":"http://localhost:8009/build_BM25",


    #===ONLINE_SERVICES===#
    "CLEAN_QUERY":"http://localhost:8010/clean_query",
    "Vectorize_Tfidf":"http://localhost:8011/vectorize_tfidf",
    "Vectorize_Embedding":"http://localhost:8012/vectorize_embedding",
    "Vectorize_Hybrid":"http://localhost:8013/vectorize_hybrid",
    "Vectorize_Bm25":"http://localhost:8014/vectorize_bm25",
    "Ranking":"http://localhost:8015/rank",
    "GET_DOCS_TEXTS":"http://localhost:8020/get_docs_texts",
    "LIGHT_CLEAN_QUERY":"http://localhost:8025/light_clean_query",
    "HYBRID_CLEAN_QUERY":"http://localhost:8026/clean_query_hybrid",
    # "SUGGESTIONS":"http://localhost:8027/suggestions",
    # "AUTO_COMPLETE":"http://localhost:8028/autocomplete",


    #====Documents_PIPELINES====#

    "TFIDF_PIPELINE":"http://localhost:8000/run_tfidf_pipeline",
    "EMBEDDING_PIPELINE":"http://localhost:8007/run_embedding_pipeline",
    "HYBRID_PIPELINE":"http://localhost:8008/run_hybrid_pipeline",
    "BM25_PIPELINE":"http://localhost:8022/run_bm25_pipeline",

    #====Queries_PIPELINES====#

    "QUERY_TFIDF_PIPELINE":"http://localhost:8016/run_query_tfidf",
    "QUERY_HYBRID_PIPELINE":"http://localhost:8017/run_query_hybrid",
    "QUERY_EMBEDDING_PIPELINE":"http://localhost:8018/run_query_embedding",
    "QUERY_BM25_PIPELINE":"http://localhost:8021/run_query_bm25",



    #===ADDITION===#
    "BUILD_INDEX_FAISS":"http://localhost:8023/build_faiss_index",
    "Ranking_FAISS":"http://localhost:8024/ranking_faiss",

}

#====BATCH_SIZE=====#

BATCH_SIZE = 10000