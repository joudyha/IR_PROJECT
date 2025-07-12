@echo off
echo Starting Hybrid services...

@REM start cmd /k "py -m uvicorn services.offline.load_services:app --port 8001 --reload"
start cmd /k "py -m uvicorn services.offline.representations.Hybrid_representation_service:app --port 8005 --reload"

start cmd /k "py -m uvicorn services.offline.query_hybrid_clean_service:app --port 8010 --reload"
start cmd /k "py -m uvicorn services.online.representations.query_Hybrid_representation_service:app --port 8013 --reload"
start cmd /k "py -m uvicorn services.online.ranking_service:app --port 8015 --reload"
start cmd /k "py -m uvicorn services.online.get_docs_text_service:app --port 8020 --reload"


start cmd /k "py -m uvicorn services.offline.full_structure.document_hybrid_pipeline:app --port 8008 --reload"
start cmd /k "py -m uvicorn services.online.full_structure.query_hybrid_pipeline:app --port 8017 --reload"

echo Hybrid services started.
pause
