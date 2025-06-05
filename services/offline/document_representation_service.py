from fastapi import FastAPI
from pydantic import BaseModel
from utils.representers.initialize_representer import get_representer

app = FastAPI()

class RepresentationRequest(BaseModel):
    representation_type: str
    text: str
    dataset_name: str

@app.post("/represent_text")
def represent_text(request: RepresentationRequest):
    try:
        representer = get_representer(request.representation_type, request.dataset_name)
        if not representer:
            return {"error": f"Unsupported representation type: {request.representation_type}"}
        
        vector = representer.represent(request.text)
        return {
            "representation_type": request.representation_type,
            "dataset_name": request.dataset_name,
            "vector": vector.tolist(),
            "dimension": len(vector)
        }
    except FileNotFoundError as e:
        return {"error": str(e)}
