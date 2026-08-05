from flask import Blueprint

from controllers.chat_controller import ask_question, chat_list, start_chat, chat_messages

chat_bp = Blueprint("chat", __name__)

chat_bp.route("/start", methods=["POST"])(start_chat)
chat_bp.route("/list", methods=["POST"])(chat_list)
chat_bp.route("/ask-question", methods=["POST"])(ask_question)
chat_bp.route("/messages", methods=["POST"])(chat_messages)