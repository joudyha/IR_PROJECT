from sentence_transformers import CrossEncoder,SentenceTransformer


model = SentenceTransformer('all-MiniLM-L6-v2')

# خزنه داخل utils/embedding_models
model.save('Bert_model/all-MiniLM-L6-v2')

model = SentenceTransformer("sentence-transformers/multi-qa-MiniLM-L6-cos-v1")
model.save("Bert_model/multi-qa-MiniLM-L6-cos-v1")

cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

# 2. تخزينه محلياً
cross_encoder.save("Bert_model/ms-marco-MiniLM-L-6-v2")

