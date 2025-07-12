import re
import os
import nltk
import sqlite3
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
import threading
from nltk.corpus import stopwords, wordnet
from utils.middleware_cors_config import add_cors
from utils.config import SQLITE_DB_PATH
from typing import Optional
from collections import Counter
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from symspellpy.symspellpy import SymSpell
from functools import lru_cache
import marisa_trie 
from symspellpy.symspellpy import Verbosity

for resource in ["stopwords", "wordnet"]:
    try:
        nltk.data.find(f"corpora/{resource}")
    except LookupError:
        nltk.download(resource)

class QueryRefiner:
    def __init__(self, processed_terms):
        self.processed_terms = set(processed_terms)
        self.term_frequencies = Counter(processed_terms)
        self.stop_words = set(stopwords.words("english"))

        self.sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
        dictionary_path = os.path.join("utils", "symspell_data", "frequency_dictionary_en_82_765.txt")
        if not self.sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1):
            raise FileNotFoundError("فشل تحميل القاموس")

        self.sym_spell.create_dictionary_entry("change", 5000)
        self.sym_spell.create_dictionary_entry("environment", 5000)
        self.sym_spell.create_dictionary_entry("surroundings", 3000)

        self.trie = marisa_trie.Trie(self.processed_terms)

    def reduce_repeated_letters(self, word):
        return re.sub(r'(.)\1{2,}', r'\1', word)

    
    def correct_spelling(self, query: str) -> str:
     query = self.reduce_repeated_letters(query.lower())
     words = query.split()
     corrected_words = []

     for word in words:
        if word in self.processed_terms or word in self.trie:
            corrected_words.append(word)
            continue

        suggestions = self.sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)
        corrected = suggestions[0].term if suggestions else word
        corrected_words.append(corrected)

     return " ".join(corrected_words)


    def suggest_correction(self, query: str) -> str:
        corrected = self.correct_spelling(query)
        return corrected if corrected.lower() != query.lower() else None

    @lru_cache(maxsize=10000)
    def get_synonyms(self, word, max_synonyms=10):
        synonyms = set()
        word = word.lower()
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                name = lemma.name().lower()
                if name != word and len(name) > 2 and name.isalpha():
                    synonyms.add(name.replace("_", " "))
                    if len(synonyms) >= max_synonyms:
                        return list(synonyms)
        return list(synonyms)

    def expand_query(self, query):
        corrected = self.correct_spelling(query)
        words = corrected.lower().split()
        expanded_terms = set()

        for word in words:
            if word in self.stop_words:
                continue
            expanded_terms.add(word)
            expanded_terms.update(self.get_synonyms(word))

        return " ".join(expanded_terms) if expanded_terms else query

    def autocomplete(self, prefix, max_suggestions=5):
        prefix = prefix.lower()
        matches = self.trie.keys(prefix)
        return sorted(matches, key=lambda x: self.term_frequencies.get(x, 0), reverse=True)[:max_suggestions]

app = FastAPI()
add_cors(app)

class SuggestionsRequest(BaseModel):
    query: str
    dataset_name: str
    chosen_option: str = "original"

class SuggestionsResponse(BaseModel):
    corrected_query: Optional[str] = None
    expanded_query: str
    dynamic_suggestions: Optional[Dict[str, list]] = None  # هنا جعلته اختياري
    final_query: str

class AutocompleteRequest(BaseModel):
    prefix: str
    dataset_name: str

refiner_lock = threading.Lock()
refiners_cache = {}

def fetch_processed_texts_from_db(dataset_name):
    conn = sqlite3.connect(SQLITE_DB_PATH)
    query = """
        SELECT processed_text
        FROM docs
        WHERE dataset_name = ? AND processed_text IS NOT NULL
    """
    df = pd.read_sql(query, conn, params=(dataset_name,))
    conn.close()
    return df["processed_text"].tolist()
def reduce_repeated_letters(word):
    return re.sub(r'(.)\1{2,}', r'\1', word)

def build_processed_terms(processed_texts, min_freq=2):
    words = []
    for text in processed_texts:
        for w in text.split():
            clean_w = reduce_repeated_letters(w)
            words.append(clean_w)
    term_freq = Counter(words)
    return [word for word, freq in term_freq.items() if freq >= min_freq]
def get_or_create_refiner(dataset_name):
    with refiner_lock:
        if dataset_name not in refiners_cache:
            processed_texts = fetch_processed_texts_from_db(dataset_name)
            processed_terms = build_processed_terms(processed_texts)
            refiners_cache[dataset_name] = QueryRefiner(processed_terms)
        return refiners_cache[dataset_name]

@app.post("/suggestions", response_model=SuggestionsResponse)
async def get_suggestions(req: SuggestionsRequest):
    refiner = get_or_create_refiner(req.dataset_name)
    correction = refiner.suggest_correction(req.query)
    correction = correction if correction is not None and correction.lower() != req.query.lower() else None
    expanded_query = refiner.expand_query(req.query)

    if req.chosen_option == "corrected":
        final_query = correction
    elif req.chosen_option == "expanded":
        final_query = expanded_query
    else:
        final_query = req.query

    return {
        "corrected_query": correction,
        "expanded_query": expanded_query,
        "final_query": final_query
    }

@app.post("/autocomplete")
async def get_autocomplete(req: AutocompleteRequest):
    refiner = get_or_create_refiner(req.dataset_name)
    suggestions = refiner.autocomplete(req.prefix)
    return {"prefix": req.prefix, "suggestions": suggestions}