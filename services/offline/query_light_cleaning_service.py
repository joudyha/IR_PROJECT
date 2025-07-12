
from fastapi import FastAPI
from pydantic import BaseModel
from utils.clean_text import light_clean
from utils.middleware_cors_config import add_cors 

app = FastAPI()
add_cors(app)
class TextInput(BaseModel):
    query: str

@app.post("/light_clean_query")
def clean_query(input: TextInput):
    cleaned = light_clean(input.query)
    tokens = cleaned.split()

    return {"query_tokens": tokens,"raw_query":input.query}