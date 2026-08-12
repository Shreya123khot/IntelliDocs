from flask import request, jsonify
from database import get_connection
from flask_jwt_extended import create_access_token


def register():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    usertype = "user"

    if not name or not email or not password:
        return jsonify({
            "success": False,
            "message": "All fields are required."
        }), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Check existing email
    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (email,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        conn.close()

        return jsonify({
            "success": False,
            "message": "Email already registered."
        }), 409


    # Insert user
    sql = """
    INSERT INTO users(name, email, password, usertype)
    VALUES(%s,%s,%s,%s)
    """

    cursor.execute(
        sql,
        (name, email, password, usertype)
    )

    conn.commit()

    user_id = cursor.lastrowid

    cursor.close()
    conn.close()


    return jsonify({
        "success": True,
        "message": "Registration successful.",
        "user": {
            "id": user_id,
            "name": name,
            "email": email,
            "usertype": usertype
        }
    }), 201



def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")


    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password required."
        }),400


    conn = get_connection()
    cursor = conn.cursor(dictionary=True)


    sql = """
    SELECT * FROM users
    WHERE email=%s AND password=%s
    """

    cursor.execute(
        sql,
        (email, password)
    )

    user = cursor.fetchone()


    cursor.close()
    conn.close()


    if user:

        # Create JWT Token
        token = create_access_token(
            identity=user["email"]
        )


        return jsonify({
            "success": True,
            "message": "Login successful.",
            "access_token": token,
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "usertype": user["usertype"]
            }
        }),200


    else:

        return jsonify({
            "success": False,
            "message": "Invalid email or password."
        }),401