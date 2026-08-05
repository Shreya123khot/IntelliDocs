from flask import Blueprint

from controllers.document_controller import upload_document

documents_bp = Blueprint("documents", __name__)

documents_bp.route("/upload", methods=["POST"])(upload_document)