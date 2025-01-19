from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.services.user_service import create_user, get_all_users, get_user_by_username, get_user_by_id
from app.extensions import bcrypt
from app.models.user import User



user_bp = Blueprint("user", __name__)


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user_data = get_user_by_username(username)

        if not user_data or 'password_hash' not in user_data:
            error_message = "Nom d'utilisateur ou mot de passe incorrect"
            return render_template('login.html', error=error_message)

        if not bcrypt.check_password_hash(user_data['password_hash'], password):
            error_message = "Nom d'utilisateur ou mot de passe incorrect"
            return render_template('login.html', error=error_message)

        user = User(user_data['id'], user_data['username'], user_data['role'])
        login_user(user)
        return redirect('/users') 
    return render_template('login.html')



@user_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200


@user_bp.route("/")
def home():
    return "Welcome to the Secure Web App!"


@user_bp.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")

        response_message, success = create_user(username, password, role)
        if success:
            return redirect("/login")
        else:
            return jsonify({"message": "Failed to create user"}), 400
        
    return render_template("register.html")


@user_bp.route("/users", methods=["GET"])
@login_required
def list_users():
    users = get_all_users()
    return render_template("users.html", users=users)
