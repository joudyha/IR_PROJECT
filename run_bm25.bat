@echo off
echo Starting BM25 services...

@REM start cmd /k "py -m uvicorn services.offline.load_services:app --port 8001 --reload"
@REM start cmd /k "py -m uvicorn services.offline.document_preprocessing_service:app --port 8004 --reload"
start cmd /k "py -m uvicorn services.offline.representations.BM25_representation_service:app --port 8009 --reload"
start cmd /k "py -m uvicorn services.offline.inverted_index_service:app --port 8003 --reload"


@REM start cmd /k "py -m uvicorn services.online.query_cleaning_service:app --port 8010 --reload"
start cmd /k "py -m uvicorn services.online.representations.query_BM25_representation_service:app --port 8014 --reload"
start cmd /k "py -m uvicorn services.online.ranking_service:app --port 8015 --reload"
start cmd /k "py -m uvicorn services.online.get_docs_text_service:app --port 8020 --reload"



start cmd /k "py -m uvicorn services.offline.full_structure.document_bm25_pipeline:app --port 8022 --reload"
start cmd /k "py -m uvicorn services.online.full_structure.query_bm25_pipeline:app --port 8021 --reload"

echo BM25 services started.
pause
