from flask import request, jsonify
from werkzeug.utils import secure_filename
import os
import uuid

from services.document_service import (
    extract_text_from_pdf,
    extract_text_from_txt
)

from services.chunk_service import create_chunks

from services.embedding_service import generate_embeddings

from services.vector_service import store_document


UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def upload_document():

    try:

        print("FILES:", request.files)
        print("FORM:", request.form)

        file = request.files.get("file")

        if not file:
            return jsonify({
                "success": False,
                "message": "File is required"
            }), 400

        if file.filename == "":
            return jsonify({
                "success": False,
                "message": "No file selected"
            }), 400

        filename = secure_filename(file.filename)

        if not filename:
            return jsonify({
                "success": False,
                "message": "Invalid filename"
            }), 400

        # --------------------------------
        # Save file
        # --------------------------------

        document_id = str(uuid.uuid4())

        file_path = os.path.join(
            UPLOAD_FOLDER,
            document_id + "_" + filename
        )

        file.save(file_path)

        # --------------------------------
        # Extract text
        # --------------------------------

        extension = os.path.splitext(
            filename
        )[1].lower()

        if extension == ".pdf":

            text = extract_text_from_pdf(
                file_path
            )

        elif extension == ".txt":

            text = extract_text_from_txt(
                file_path
            )

        else:

            return jsonify({
                "success": False,
                "message": "Only PDF and TXT files are supported"
            }), 400

        if not text or not text.strip():

            return jsonify({
                "success": False,
                "message": "Could not extract text from document"
            }), 400

        # --------------------------------
        # Create chunks
        # --------------------------------

        chunks = create_chunks(text)

        if not chunks:

            return jsonify({
                "success": False,
                "message": "Could not create document chunks"
            }), 500

        # --------------------------------
        # Generate embeddings
        # --------------------------------

        embeddings = generate_embeddings(
            chunks
        )

        # --------------------------------
        # Store in vector database
        # --------------------------------

        store_document(
            document_id,
            chunks,
            embeddings
        )

        # --------------------------------
        # Success
        # --------------------------------

        return jsonify({

            "success": True,

            "message": "Document uploaded successfully",

            "document_id": document_id,

            "filename": filename,

            "chunks": len(chunks)

        }), 200

    except Exception as e:

        print("UPLOAD ERROR:", str(e))

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500