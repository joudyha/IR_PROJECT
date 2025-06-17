@echo off
echo Starting Embedding services...

start cmd /k "py -m uvicorn services.offline.load_services:app --port 8001 --reload"
start cmd /k "py -m uvicorn services.offline.document_preprocessing_service:app --port 8004 --reload"
start cmd /k "py -m uvicorn services.offline.representations.embedding_representation_service:app --port 8006 --reload"

start cmd /k "py -m uvicorn services.online.query_cleaning_service:app --port 8010 --reload"
start cmd /k "py -m uvicorn services.online.representations.query_embedding_representation_service:app --port 8012 --reload"
start cmd /k "py -m uvicorn services.online.ranking_service:app --port 8015 --reload"
start cmd /k "py -m uvicorn services.online.get_docs_text_service:app --port 8020 --reload"



start cmd /k "py -m uvicorn full_structure.embedding_pipeline.document_embedding_pipeline:app --port 8007 --reload"
start cmd /k "py -m uvicorn full_structure.embedding_pipeline.query_embedding_pipeline:app --port 8018 --reload"

echo Embedding services started.
pause
