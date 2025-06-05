from fastapi import FastAPI
from pydantic import BaseModel
from utils.clean_text import clean_text

app = FastAPI()

class TextInput(BaseModel):
    query: str

@app.post("/clean")
def clean_query(input: TextInput):
    cleaned = clean_text(input.query)
    return {"cleaned_text": cleaned}