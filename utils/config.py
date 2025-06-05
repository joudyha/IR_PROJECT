

#=====SQLITE_DB=====#
SQLITE_DB_PATH="datasets.db"


#=====SERVICES_URL=====#

SERVICES_URL={
    "LOAD_RAW_DOCS":"http://localhost:8001/load_raw_docs",
    "CLEAN_STORED_DOCS":"http://localhost:8004/clean_stored_docs",
    "BUILD_TFIDF":"http://localhost:8002/build_tfidf",
    "INVERTED_INDEX":"http://localhost:8003/build_inverted_index"
}

#====BATCH_SIZE=====#

BATCH_SIZE = 100