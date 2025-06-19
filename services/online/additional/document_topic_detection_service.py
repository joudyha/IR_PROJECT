import sqlite3
import pyLDAvis
import pandas as pd
import pyLDAvis.gensim
from fastapi import  FastAPI,Query
from gensim.models import LdaModel, CoherenceModel
from gensim.corpora import Dictionary
from gensim.models.phrases import Phraser
import pyLDAvis
import pyLDAvis.gensim
from utils.config import SQLITE_DB_PATH


app=FastAPI()

@app.post('/topic_detection')
def topic_detection(dataset_name:str=Query(...)):
    conn = sqlite3.connect(SQLITE_DB_PATH)
    df = pd.read_sql("""
           SELECT doc_id, processed_text 
           FROM docs 
           WHERE dataset_name = ? AND processed_text IS NOT NULL
       """, conn, params=(dataset_name,))

    if df.empty:
        return {"error": f"No documents found for dataset '{dataset_name}'"}
    tokenized_corpus = [doc.split() for doc in df['processed_text']]
    from gensim.models import Phrases
    bigram = Phrases(tokenized_corpus, min_count=5, threshold=30)
    bigram_mod = Phraser(bigram)
    trigram = Phrases(bigram[tokenized_corpus], min_count=5, threshold=40)
    trigram_mod = Phraser(trigram)
    docs_with_bigrams = [bigram_mod[doc] for doc in tokenized_corpus]
    docs_with_trigrams = [trigram_mod[bigram_mod[doc]] for doc in tokenized_corpus]

    dictionary = Dictionary(docs_with_bigrams)
    dictionary.filter_extremes(no_below=3, no_above=0.7)
    corpus = [dictionary.doc2bow(doc)  for doc in docs_with_bigrams]
    lda_model = LdaModel(corpus=corpus,
                         id2word=dictionary,
                         num_topics=6,
                         passes=200,
                         alpha='auto',
                         eta='auto',
                         chunksize=200,
                         random_state=42
                         )

    coherence_model = CoherenceModel(model=lda_model, texts=docs_with_bigrams, dictionary=dictionary, coherence='c_v')
    coherence_score = coherence_model.get_coherence()
    lda_vis = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary)
    pyLDAvis.save_html(lda_vis, 'lda_visualization.html')

    return f"topic detection complete on {dataset_name} with coherance {coherence_score}"




