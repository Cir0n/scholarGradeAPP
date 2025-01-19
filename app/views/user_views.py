from flask import (Blueprint, jsonify, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required, login_user, logout_user

from app.extensions import bcrypt
from app.models.user import User
from app.services.student_service import get_all_students
from app.services.user_service import create_user, verify_user_credentials

user_bp = Blueprint("user", __name__)


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        response = verify_user_credentials(username, password)
        if "error" in response:
            return render_template("login.html", error=response["error"])

        user_data = response["data"]
        print(f"Login successful for user: {user_data}")
        user = User(user_data["id"], user_data["username"], user_data["role"])
        login_user(user)

        if user.role == "student":
            return redirect("/users")
        elif user.role == "teacher":
            return redirect("/add-grade")

    return render_template("login.html")


@user_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200


@user_bp.route("/")
def home():
    return "Welcome to the Secure Web App!"


@user_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        extra_data = request.form.get("extra_data")

        response = create_user(
            first_name, last_name, username, password, role, extra_data
        )
        if "error" in response:
            return render_template("register.html", response_message=response)
        else:
            return redirect("/login")

    return render_template("register.html")


@user_bp.route("/users", methods=["GET"])
@login_required
def list_users():
    users = get_all_students()
    return render_template("users.html", users=users)
