from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from routes.auth import auth_bp
from routes.document import document_bp
from routes.chat import chat_bp


app = Flask(__name__)

# ==========================================
# CONFIGURATION
# ==========================================

app.config["JWT_SECRET_KEY"] = "intellidocs-secret-key-2026"

# ==========================================
# CORS
# ==========================================

CORS(app)

# ==========================================
# JWT
# ==========================================

jwt = JWTManager(app)

# ==========================================
# BLUEPRINTS
# ==========================================

app.register_blueprint(
    auth_bp,
    url_prefix="/auth"
)

app.register_blueprint(
    document_bp,
    url_prefix="/document"
)

app.register_blueprint(
    chat_bp,
    url_prefix="/chat"
)

# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():
    return {
        "success": True,
        "message": "IntelliDocs API is running"
    }


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )