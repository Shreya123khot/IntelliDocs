import chromadb
import uuid
import os

# Debug
print("=" * 60)
print("Current Working Directory:", os.getcwd())
print("Chroma Path:", os.path.abspath("chroma_db"))
print("=" * 60)

# Create/Open Chroma Database
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="company_documents"
)


def store_document(document_id, chunks, embeddings):
    try:
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

        print("=" * 60)
        print("✅ Document Stored Successfully")
        print("Document ID:", document_id)
        print("Chunks Stored:", len(chunks))
        print("Collection Count:", collection.count())
        print("=" * 60)

    except Exception as e:
        print("❌ Store Error:", str(e))
        raise


def search_documents(question_embedding, top_k=3):
    try:

        print("=" * 60)
        print("Collection Count:", collection.count())
        print("Searching Top:", top_k)
        print("=" * 60)

        result = collection.query(
            query_embeddings=[question_embedding],
            n_results=top_k
        )

        print("=" * 60)
        print("Search Result:")
        print(result)
        print("=" * 60)

        return result

    except Exception as e:
        print("❌ Search Error:", str(e))
        raise