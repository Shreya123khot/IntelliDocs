from flask import request, jsonify
from database import get_connection
import uuid
from werkzeug.utils import secure_filename
import os
from services.chunk_service import create_chunks
from services.document_service import extract_text_from_pdf, extract_text_from_txt
from services.embedding_service import generate_embeddings
from services.vector_service import store_document

def upload_document():  
    title = request.form.get("title")
    document_type = request.form.get("document_type")
    file = request.files.get("file")

    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4()}_{filename}"
    
    #1. Save the uploaded file to the server
    UPLOAD_FOLDER = "uploads"
    filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
    file.save(filepath)

    #2. Extract text content based on document type
    text_content = ""
    if document_type == "pdf":
        text_content = extract_text_from_pdf(filepath)
    else:
        text_content = extract_text_from_txt(filepath)

    #3. Create chunks of text content
    chunks = create_chunks(text_content)

    #4. Create embeddings for each chunk and store them in the vector database
    vectors = generate_embeddings(chunks)
    store_document(unique_filename, chunks, vectors)
    
    sql = "INSERT INTO documents(title, document_type, filename, status) "
    sql += "VALUES('" + title + "', '" + document_type + "', '" + unique_filename + "', 'PROCESSED')"
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({
        "success": True,
        "message": "Document uploaded successfully."
    }), 201