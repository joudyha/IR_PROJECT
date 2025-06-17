@echo off
echo Starting TF-IDF services...

start cmd /k "py -m uvicorn services.offline.load_services:app --port 8001 --reload"
start cmd /k "py -m uvicorn services.offline.document_preprocessing_service:app --port 8004 --reload"
start cmd /k "py -m uvicorn services.offline.representations.tfidf_representation_service:app --port 8002 --reload"
start cmd /k "py -m uvicorn services.offline.inverted_index_service:app --port 8003 --reload"

start cmd /k "py -m uvicorn services.online.query_cleaning_service:app --port 8010 --reload"
start cmd /k "py -m uvicorn services.online.representations.query_tfidf_representation_service:app --port 8011 --reload"
start cmd /k "py -m uvicorn services.online.ranking_service:app --port 8015 --reload"
start cmd /k "py -m uvicorn services.online.get_docs_text_service:app --port 8020 --reload"


start cmd /k "py -m uvicorn full_structure.tfidf_pipeline.document_tfidf_pipeline:app --port 8000 --reload"
start cmd /k "py -m uvicorn full_structure.tfidf_pipeline.query_tfidf_pipeline:app --port 8016 --reload"

echo TF-IDF services started.
pause
