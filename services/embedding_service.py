from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

def generate_embeddings(chunks):
    embeddings = embedding_model.encode(chunks)
    return embeddings

def create_question_embedding(question):
    embedding = embedding_model.encode(question)
    return embedding.tolist()