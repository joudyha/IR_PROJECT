@echo off
echo start services..

@REM start cmd /k "py -m uvicorn services.offline.load_services:app --port 8001 --reload"
@REM start cmd /k "py -m uvicorn services.offline.document_preprocessing_service:app --port 8004 --reload"
@REM start cmd /k "py -m uvicorn services.offline.inverted_index_service:app --port 8003 --reload"
start cmd /k "py -m uvicorn services.offline.query_cleaning_service:app --port 8010 --reload"
start cmd /k "py -m uvicorn services.online.ranking_service:app --port 8015 --reload"
start cmd /k "py -m uvicorn services.online.get_docs_text_service:app --port 8020 --reload"


start cmd /k "py -m uvicorn services.offline.query_hybrid_clean_service:app --port 8026 --reload"
start cmd /k "py -m uvicorn services.offline.query_light_cleaning_service:app --port 8025 --reload"


@REM start cmd /k "py -m uvicorn services.offline.representations.tfidf_representation_service:app --port 8002 --reload"
@REM start cmd /k "py -m uvicorn services.offline.representations.BM25_representation_service:app --port 8009 --reload"
start cmd /k "py -m uvicorn services.offline.representations.Hybrid_representation_service:app --port 8005 --reload"
@REM start cmd /k "py -m uvicorn services.offline.representations.embedding_representation_service:app --port 8006 --reload"



start cmd /k "py -m uvicorn services.online.representations.query_tfidf_representation_service:app --port 8011 --reload"
start cmd /k "py -m uvicorn services.online.representations.query_BM25_representation_service:app --port 8014 --reload"
start cmd /k "py -m uvicorn services.online.representations.query_embedding_representation_service:app --port 8012 --reload"
start cmd /k "py -m uvicorn services.online.representations.query_Hybrid_representation_service:app --port 8013 --reload"








start cmd /k "py -m uvicorn services.offline.full_structure.document_tfidf_pipeline:app --port 8000 --reload"
start cmd /k "py -m uvicorn services.online.full_structure.query_tfidf_pipeline:app --port 8016 --reload"
start cmd /k "py -m uvicorn services.offline.full_structure.document_bm25_pipeline:app --port 8022 --reload"
start cmd /k "py -m uvicorn services.online.full_structure.query_bm25_pipeline:app --port 8021 --reload"
start cmd /k "py -m uvicorn services.offline.full_structure.document_embedding_pipeline:app --port 8007 --reload"
start cmd /k "py -m uvicorn services.online.full_structure.query_embedding_pipeline:app --port 8018 --reload"
start cmd /k "py -m uvicorn services.offline.full_structure.document_hybrid_pipeline:app --port 8008 --reload"
start cmd /k "py -m uvicorn services.online.full_structure.query_hybrid_pipeline:app --port 8017 --reload"





@REM start cmd /k "py -m uvicorn addition.vector_store.build_faiss_index:app --port 8023 --reload"
start cmd /k "py -m uvicorn addition.vector_store.ranking_faiss:app --port 8024 --reload"
start cmd /k "py -m uvicorn addition.Query_Refinement.QueryRefiner:app --port 8027 --reload"
start cmd /k "py -m uvicorn addition.topic_detection.document_topic_detection_service:app --port 8029 --reload"

pause
