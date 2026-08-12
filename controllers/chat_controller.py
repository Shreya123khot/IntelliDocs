from flask import request, jsonify

from database import get_connection

from services.chunk_service import get_context
from services.embedding_service import create_question_embedding
from services.vector_service import search_documents
from services.llm_service import (
    ask_question_to_ollama,
    build_prompt
)


# =========================================================
# START CHAT
# =========================================================

def start_chat():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "message": "Invalid JSON"
        }), 400

    userid = data.get("userid")
    title = data.get("title")

    if not userid or not title:
        return jsonify({
            "success": False,
            "message": "userid and title required"
        }), 400

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO chats (userid, title)
        VALUES (%s, %s)
        """

        cursor.execute(
            sql,
            (userid, title)
        )

        conn.commit()

        chat_id = cursor.lastrowid

        return jsonify({
            "success": True,
            "message": "Chat started successfully",
            "chat_id": chat_id
        }), 201

    except Exception as e:

        if conn:
            conn.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# =========================================================
# ASK QUESTION
# =========================================================

def ask_question():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "message": "Invalid JSON"
        }), 400

    question = data.get("question")
    chat_id = data.get("chat_id")

    if not question:
        return jsonify({
            "success": False,
            "message": "Question required"
        }), 400

    conn = None
    cursor = None

    try:

        # -------------------------------------------------
        # 1. Create Question Embedding
        # -------------------------------------------------

        question_embedding = create_question_embedding(
            question
        )

        # -------------------------------------------------
        # 2. Search Similar Documents
        # -------------------------------------------------

        documents = search_documents(
            question_embedding
        )

        # -------------------------------------------------
        # 3. Extract Context
        # -------------------------------------------------

        context = get_context(
            documents
        )

        # -------------------------------------------------
        # 4. Build Prompt
        # -------------------------------------------------

        prompt = build_prompt(
            context,
            question
        )

        # -------------------------------------------------
        # 5. Ask Ollama
        # -------------------------------------------------

        answer = ask_question_to_ollama(
            prompt
        )

        # -------------------------------------------------
        # 6. Save Chat Message
        # -------------------------------------------------

        if chat_id:

            conn = get_connection()
            cursor = conn.cursor()

            sql = """
            INSERT INTO chat_messages
            (
                chat_id,
                question,
                answer
            )
            VALUES
            (
                %s,
                %s,
                %s
            )
            """

            cursor.execute(
                sql,
                (
                    chat_id,
                    question,
                    answer
                )
            )

            conn.commit()

        # -------------------------------------------------
        # 7. Return Answer
        # -------------------------------------------------

        return jsonify({
            "success": True,
            "answer": answer
        }), 200

    except Exception as e:

        if conn:
            conn.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# =========================================================
# CHAT LIST
# =========================================================

def chat_list():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "message": "Invalid JSON"
        }), 400

    userid = data.get("userid")

    if not userid:
        return jsonify({
            "success": False,
            "message": "userid required"
        }), 400

    conn = None
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor(
            dictionary=True
        )

        sql = """
        SELECT
            id,
            userid,
            title,
            created_at
        FROM chats
        WHERE userid = %s
        ORDER BY id DESC
        """

        cursor.execute(
            sql,
            (userid,)
        )

        chats = cursor.fetchall()

        return jsonify({
            "success": True,
            "chats": chats
        }), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# =========================================================
# CHAT MESSAGES
# =========================================================

def chat_messages():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "message": "Invalid JSON"
        }), 400

    chat_id = data.get("chat_id")

    if not chat_id:
        return jsonify({
            "success": False,
            "message": "chat_id required"
        }), 400

    try:

        messages = chat_history(
            chat_id
        )

        return jsonify({
            "success": True,
            "messages": messages
        }), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# CHAT HISTORY
# =========================================================

def chat_history(chat_id):

    conn = None
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor(
            dictionary=True
        )

        sql = """
        SELECT
            id,
            chat_id,
            question,
            answer,
            created_at
        FROM chat_messages
        WHERE chat_id = %s
        ORDER BY id ASC
        """

        cursor.execute(
            sql,
            (chat_id,)
        )

        messages = cursor.fetchall()

        return messages

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()