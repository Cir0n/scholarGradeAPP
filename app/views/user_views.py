from flask import Blueprint, jsonify, request

from app.services.user_service import create_user, get_all_users

user_bp = Blueprint("user", __name__)


@user_bp.route("/")
def home():
    return "Welcome to the Secure Web App!"


@user_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]
    password = data["password"]
    role = data.get("role", "student")

    if create_user(username, password, role):
        return jsonify({"message": "User created successfully"}), 201
    else:
        return jsonify({"message": "Failed to create user"}), 400


@user_bp.route("/users", methods=["GET"])
def list_users():
    users = get_all_users()
    return jsonify(users), 200
