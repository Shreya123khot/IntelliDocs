def create_chunks(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


def get_context(result):
    """
    Extract context safely from ChromaDB search result.
    """

    # If result is empty
    if not result:
        return ""

    # Get documents
    documents = result.get("documents", [])

    # No documents found
    if len(documents) == 0:
        return ""

    # First search result empty
    if len(documents[0]) == 0:
        return ""

    # Join all retrieved chunks
    context = "\n\n".join(documents[0])

    return context