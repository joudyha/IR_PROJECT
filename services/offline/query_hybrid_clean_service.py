from fastapi import FastAPI
from pydantic import BaseModel
from utils.clean_text import clean_text, light_clean
from utils.middleware_cors_config import add_cors 

app = FastAPI()
add_cors(app)

class TextInput(BaseModel):
    query: str

@app.post("/clean_query_hybrid")
def clean_query_hybrid(input: TextInput):
    heavy_tokens = clean_text(input.query) 
    light_cleaned = light_clean(input.query) 
    light_tokens = light_cleaned.split()      

    return {
        "heavy_tokens": heavy_tokens,
        "light_tokens": light_tokens,
        "light_text": light_cleaned
    }
