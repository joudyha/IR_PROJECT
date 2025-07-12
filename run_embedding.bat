@echo off
echo Starting Embedding services...

@REM start cmd /k "py -m uvicorn services.offline.load_services:app --port 8001 --reload"
@REM start cmd /k "py -m uvicorn services.offline.document_preprocessing_service:app --port 8004 --reload"
@REM start cmd /k "py -m uvicorn services.offline.representations.embedding_representation_service:app --port 8006 --reload"
start cmd /k "py -m uvicorn addition.vector_store.build_faiss_index:app --port 8023 --reload"
start cmd /k "py -m uvicorn addition.vector_store.ranking_faiss:app --port 8024 --reload"
start cmd /k "py -m uvicorn addition.Query_Refinement.QueryRefiner:app --port 8027 --reload"



start cmd /k "py -m uvicorn services.offline.query_light_cleaning_service:app --port 8025 --reload"
start cmd /k "py -m uvicorn services.online.representations.query_embedding_representation_service:app --port 8012 --reload"
start cmd /k "py -m uvicorn services.online.ranking_service:app --port 8015 --reload"
start cmd /k "py -m uvicorn services.online.get_docs_text_service:app --port 8020 --reload"



start cmd /k "py -m uvicorn services.offline.full_structure.document_embedding_pipeline:app --port 8007 --reload"
start cmd /k "py -m uvicorn services.online.full_structure.query_embedding_pipeline:app --port 8018 --reload"

echo Embedding services started.
pause
