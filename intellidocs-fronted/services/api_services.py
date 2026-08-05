import requests

BASE_URL = "http://127.0.0.1:5000"


def login(email, password):

    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": email,
            "password": password
        }
    )
    return response.json()

def register(name, email, password):
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "name": name,
            "email": email,
            "password": password
        }
    )
    return response.json()

def start_chat(userid, title):
    response = requests.post(
        f"{BASE_URL}/chat/start",
        json={
            "userid": userid,
            "title": title
        }
    )
    return response.json()


def ask_question(chatid, userid, question):

    response = requests.post(
        f"{BASE_URL}/chat/ask-question",
        json={
            "chatid":chatid,
            "userid":userid,
            "question": question
        }
    )

    return response.json()

def upload_document(title, document_type, file):
    files = {
        "file": (file.name, file, file.type)
    }
    data = {
        "title": title,
        "document_type": document_type
    }
    response = requests.post(
        f"{BASE_URL}/documents/upload",
        data=data,
        files=files
    )

    return response.json()

def get_chat_list(userid):
    response = requests.post(
        f"{BASE_URL}/chat/list",
        json={
            "userid": userid
        }
    )
    return response.json()

def get_chat_messages(chatid):
    response = requests.post(
        f"{BASE_URL}/chat/messages",
        json={
            "chatid": chatid
        }
    )
    return response.json()
