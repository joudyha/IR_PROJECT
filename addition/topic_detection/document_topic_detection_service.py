import sqlite3
import pyLDAvis
import pandas as pd
import pyLDAvis.gensim
from fastapi import FastAPI, Query
from gensim.models import LdaModel, CoherenceModel
from gensim.corpora import Dictionary
from gensim.models.phrases import Phraser, Phrases
from utils.config import SQLITE_DB_PATH
from tqdm import tqdm
from pyLDAvis import prepared_data_to_html

app = FastAPI()

@app.post('/topic_detection')
def topic_detection(dataset_name: str = Query(...)):
    conn = sqlite3.connect(SQLITE_DB_PATH)
    df = pd.read_sql("""
           SELECT doc_id, processed_text 
           FROM docs 
           WHERE dataset_name = ? AND processed_text IS NOT NULL
       """, conn, params=(dataset_name,))

    if df.empty:
        return {"error": f"No documents found for dataset '{dataset_name}'"}

    tokenized_corpus = [doc.split() for doc in df['processed_text']]

    for doc in tqdm(tokenized_corpus, desc="Tokenizing corpus"):
        pass

    bigram = Phrases(tokenized_corpus, min_count=5, threshold=30)
    bigram_mod = Phraser(bigram)
    trigram = Phrases(bigram[tokenized_corpus], min_count=5, threshold=40)
    trigram_mod = Phraser(trigram)

    docs_with_bigrams = [bigram_mod[doc] for doc in tqdm(tokenized_corpus, desc="Applying bigrams")]
    docs_with_trigrams = [trigram_mod[bigram_mod[doc]] for doc in tqdm(tokenized_corpus, desc="Applying trigrams")]

    print("Building dictionary...")
    dictionary = Dictionary(docs_with_trigrams)
    dictionary.filter_extremes(no_below=3, no_above=0.7)
    print(f"Dictionary size: {len(dictionary)}")

    print("Converting documents to bag-of-words corpus...")
    corpus = [dictionary.doc2bow(doc) for doc in docs_with_trigrams]

    print("Training LDA model...")
    num_topics =3
    lda_model = LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=num_topics,
        passes=10,
        alpha='auto',
        eta='auto',
        chunksize=200,
        random_state=42,
        eval_every=1
    )

    print("LDA model training completed.")
    print("Calculating coherence score...")
    coherence_model = CoherenceModel(
        model=lda_model,
        texts=docs_with_trigrams,
        dictionary=dictionary,
        coherence='c_v'
    )
    coherence_score = coherence_model.get_coherence()
    print(f"Coherence score: {coherence_score:.4f}")

    print("Preparing visualization...")
    vis_file = f"{dataset_name}_lda_vis{num_topics}.html"
    lda_vis = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary)
    
    html_body = prepared_data_to_html(lda_vis)
    html_with_coherence = html_body.replace(
    "</body>", 
    f"<div style='padding:10px; font-size:16px; color:#444; background:#f8f8f8; border-top:1px solid #ddd; text-align:center;'>Coherence Score: <strong>{coherence_score:.4f}</strong></div>\n</body>"
    )

    with open(vis_file, "w", encoding="utf-8") as f:
        f.write(html_with_coherence)

    print(f"Visualization saved to {vis_file}")

    return {
        "message": f"Topic detection completed for '{dataset_name}'",
        "coherence_score": coherence_score,
        "num_topics": num_topics,
        "visualization_file": vis_file
    }
