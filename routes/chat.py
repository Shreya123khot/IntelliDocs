from flask import Blueprint

from controllers.chat_controller import (
    start_chat,
    ask_question,
    chat_list,
    chat_messages
)

chat_bp = Blueprint(
    "chat",
    __name__
)

# Start new chat
chat_bp.route(
    "/start",
    methods=["POST"]
)(start_chat)

# Get all chats
chat_bp.route(
    "/list",
    methods=["POST"]
)(chat_list)

# Ask question
chat_bp.route(
    "/ask-question",
    methods=["POST"]
)(ask_question)

# Get chat messages
chat_bp.route(
    "/messages",
    methods=["POST"]
)(chat_messages)