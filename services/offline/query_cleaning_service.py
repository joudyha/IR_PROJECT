from fastapi import FastAPI
from pydantic import BaseModel
from utils.clean_text import clean_text
from utils.middleware_cors_config import add_cors 

app = FastAPI()
add_cors(app)
class TextInput(BaseModel):
    query: str

@app.post("/clean_query")
def clean_query(input: TextInput):
    cleaned = clean_text(input.query)
    return {"query_tokens": cleaned}