import joblib
import numpy as np
import os

class TfidfRepresenter:
    def __init__(self, dataset_name: str):
        vectorizer_path = f"utils/joblib_files/tfidf_model/{dataset_name}_vectorizer.joblib"
        if not os.path.exists(vectorizer_path):
            raise FileNotFoundError(f"Vectorizer for dataset '{dataset_name}' not found at {vectorizer_path}")
        
        self.vectorizer, _, _ = joblib.load(vectorizer_path)

    def represent(self, text: str) -> np.ndarray:
        return self.vectorizer.transform([text]).toarray()[0]
