from flask import Blueprint
from controllers.document_controller import upload_document

document_bp = Blueprint("document", __name__)


@document_bp.route("/upload", methods=["POST"])
def upload():
    return upload_document()