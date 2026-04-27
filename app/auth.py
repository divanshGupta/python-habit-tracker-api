from flask import Blueprint, request, jsonify
from app import db, bcrypt
from app.models import User
from flask_jwt_extended import create_access_token
import logging

logger = logging.getLogger(__name__)
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        logger.warning("Register attempt with missing fields")
        return jsonify({"error": "Username and password are required"}), 400

    if len(data["password"]) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    if User.query.filter_by(username=data["username"]).first():
        logger.warning("Register attempt with taken username: %s", data["username"])
        return jsonify({"error": "Username already taken"}), 409
    
    hashed = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    user = User(username=data["username"], password=hashed)
    db.session.add(user)
    db.session.commit()
    logger.info("New user registered: %s", data["username"])
    return jsonify({"message": "User created"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        logger.warning("Login attempt with missing fields")
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=data["username"]).first()
    if not user or not bcrypt.check_password_hash(user.password, data["password"]):
        logger.warning("Failed login attempt for username: %s", data.get("username"))
        return jsonify({"error": "Invalid credentials"}), 401
    
    token = create_access_token(identity=str(user.id))
    logger.info("User logged in: %s", data["username"])
    return jsonify({"token": token})