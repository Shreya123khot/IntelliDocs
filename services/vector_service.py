import chromadb
import uuid

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="company_documents"
)

def store_document(document_id, chunks, embeddings):
    ids = []
    metadatas = []
    for i in range(len(chunks)):
        ids.append(str(uuid.uuid4()))
        metadatas.append({
            "document_id": document_id,
            "chunk_number": i + 1
        })
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

def search_documents(question_embedding, top_k = 3):
    result = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k
    )
    return result