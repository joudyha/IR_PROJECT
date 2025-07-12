
# IR_PROJECT – Intelligent Search Engine

A graduation project aimed at developing an advanced Information Retrieval (IR) system that mimics the behavior of modern search engines like Google. It leverages multiple NLP techniques, vector-based search, and a modular SOA (Service-Oriented Architecture) design.

---

## 🎯 Project Goals

- Build a search engine capable of retrieving relevant documents using different text representation methods.
- Support various similarity ranking algorithms and hybrid approaches.
- Provide additional features like query correction, expansion, autocomplete, and topic modeling.

---

## 📂 Datasets

The system supports two benchmark datasets:

- **BEIR** – ~523K documents, 5K queries.
- **ANTIQUE** – ~404K documents, 200 queries.

Each dataset includes long textual paragraphs and is categorized into topics such as education, technology, philosophy, religion, and more.

To run the system, place the datasets inside a folder named `datasets` at the **root of the project**:

```
IR_PROJECT/
├── datasets/
│   ├── beir/
│   └── antique/
```

You can download the datasets from:
- [BEIR Dataset](https://drive.google.com/drive/folders/1Q2TMOtzM8qTreqlwZbfsn57JDZsjYb9G)
- [ANTIQUE Dataset](https://drive.google.com/drive/folders/1KPkX8I8t5CD83Mzd7v0G0i9ZGRwP4FGB)

---

## ⚙️ System Architecture (SOA)

The system is built using **Service-Oriented Architecture (SOA)** and structured around modular **pipelines**. Each pipeline corresponds to a complete flow of document and query processing for a specific representation method.

### Key Design Principles:
- Each module is developed as an **independent service** (e.g., text cleaning, indexing, retrieval, ranking).
- Services communicate with each other through **clearly defined pipelines**.
- You can test **any service individually** using Postman or by running its `.bat` script.
- The full system can also be executed as one integrated workflow.

---

## 🔧 How to Run the Project

### Option 1: Run a specific representation pipeline

Use individual `.bat` files to run a specific representation-based pipeline (e.g., TF-IDF, BM25, BERT). This lets you focus on testing or improving a single component.

Example:
```bash
run_tfidf.bat
```

### Option 2: Run the complete system

Use the main script to launch the entire workflow:
```bash
run_all.bat
```

This will execute the full flow:
```
Preprocessing → Representation → Indexing → Query → Retrieval → Ranking → Results
```

---

## 🔹 System Services Overview

### Text Storage Service
- Uses SQLite for document persistence.
- Stores raw and preprocessed texts.

### Text Processing Service
- Performs both light and heavy preprocessing (cleaning, normalization, tokenization).

### Text Representation Methods
- **TF-IDF**
- **BM25**
- **Embeddings** (BERT, Word2Vec using HuggingFace)
- **Hybrid** (e.g., TF-IDF + Embeddings)

### Indexing and Retrieval
- Inverted index for sparse models (TF-IDF, BM25)
- FAISS vector index for dense models (embeddings)
- Query-document similarity via Cosine or FAISS search

### Query Services
- Query preprocessing and vectorization
- Query suggestion (autocomplete, spelling correction, expansion using WordNet)
- Reranking using cross-encoders for higher precision

### Topic Modeling
- Uses LDA to detect latent topics
- Outputs an interactive HTML report for visualization

---


## 🧪 Evaluation Highlights

- Comparison of retrieval effectiveness across different methods.
- Time and performance trade-offs between cosine similarity and vector store.
- Effects of query correction and expansion on search results.
- Topic modeling coherence scores on both datasets.

---

## 💻 Technologies Used

- Python
- SQLite
- Scikit-learn
- HuggingFace Transformers
- FAISS (Facebook AI Similarity Search)
- Gensim (LDA)
- SymSpell (spelling correction)
- Flask (API framework)

---

## 🔗 Resources

- 📂 [BEIR Dataset](https://drive.google.com/drive/folders/1Q2TMOtzM8qTreqlwZbfsn57JDZsjYb9G)
- 📂 [ANTIQUE Dataset](https://drive.google.com/drive/folders/1KPkX8I8t5CD83Mzd7v0G0i9ZGRwP4FGB)
- 💻 [GitHub Repository](https://github.com/joudyha/IR_PROJECT.git)

---

> Developed by: Ali Jihad Alali, Joudy Ayman Hamadeh, Ammar Nazir Al-Aloush, Ali Emad Mousa, Bayan Darbas, Tawfiq AL_Hammada
> Supervised by: Ms. Soulyma Mahairi ,Ms.Marwa Al_Dayah
> Damascus University – Faculty of Informatics Engineering
