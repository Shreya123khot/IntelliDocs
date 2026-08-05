from flask import request, jsonify
from database import get_connection

def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    usertype = "user"
    
    sql = "INSERT INTO users(name, email, password, usertype) "
    sql += "VALUES('" + name + "', '" + email + "', '" + password + "', '" + usertype + "')"
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({
        "success": True,
        "message": "Registration successful.",
        "user": data
    }), 201

def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    sql = "SELECT * FROM users WHERE email='" + email + "' AND password='" + password + "'"
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return jsonify({
            "success": True,
            "message": "Login successful.",
            "user": user
        }), 200
    else:   
        return jsonify({
            "success": False,
            "message": "Login failed. Invalid email or password."
        }), 401