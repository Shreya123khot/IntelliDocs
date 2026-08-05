from flask import request, jsonify
from database import get_connection
from services.chunk_service import get_context
from services.embedding_service import create_question_embedding
from services.vector_service import search_documents
from services.chunk_service import get_context
from services.llm_service import ask_question_to_ollama, build_prompt, ask_question_to_groq

def start_chat():
    data = request.get_json()
    userid = data.get("userid")
    title = data.get("title")
    sql = "INSERT INTO chats(userid, title) "
    sql += "VALUES('" + str(userid) + "', '" + title + "')"
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    chat_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Chat started successfully.",
        "chat_id": chat_id,
        "title": title
    }), 201

def ask_question(): 
    data = request.get_json()
    chatid = data.get("chatid")
    userid = data.get("userid")
    question = data.get("question")

    #1. Create embedding for the question
    embeddings = create_question_embedding(question)
    #2. Search for relevant documents in the vector database
    documents = search_documents(embeddings)
    #3. Get context from the retrieved documents
    context = get_context(documents)

    #4. Get history for chat and build prompt
    message_history = chat_history(chatid)

    prompt = build_prompt(question, context)
    #answer = ask_question_to_ollama(prompt, message_history)
    answer = ask_question_to_groq(prompt, message_history)

    sql = "INSERT INTO chat_messages(chatid, message_by, message) "
    sql += "VALUES(" + str(chatid) + ", 'user', '" + question.replace("'", "''") + "'), "
    sql += "(" + str(chatid) + ", 'llm', '" + answer.replace("'", "''") + "') "
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "success": True,
        "answer": answer
    }), 201

def chat_messages():
    data = request.get_json()
    chatid = data.get("chatid")
    messages = chat_history(chatid)

    return jsonify({
        "success": True,
        "messages": messages
    }), 201

def chat_list():
    data = request.get_json()
    userid = data.get("userid")
    sql = "SELECT * FROM chats WHERE userid = " + str(userid) + " ORDER BY id DESC"
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    chats = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify({
        "success": True,
        "chats": chats
    }), 201

def chat_history(chatid):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM chat_messages WHERE chatid = " + str(chatid) + " ORDER BY id"
    cursor.execute(sql)
    messages = cursor.fetchall()
    cursor.close()
    conn.close()
    return messages