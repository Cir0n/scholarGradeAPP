from flask import Flask

from app.extensions import bcrypt, login_manager
from app.models.user import User
from app.services.student_service import get_student_by_id
from app.services.teacher_service import get_teacher_by_id
from app.views.student_view import student_bp
from app.views.teacher_view import teacher_bp
from app.views.user_views import user_bp
from config import Config


@login_manager.user_loader
def load_user(user_id):
    print(f"Loading user with ID: {user_id}")
    user_data = get_student_by_id(user_id)
    if user_data:
        print(f"User found in students: {user_data['username']}")
        return User(user_data["id"], user_data["username"], "student")

    user_data = get_teacher_by_id(user_id)
    if user_data:
        print(f"User found in teachers: {user_data['username']}")
        return User(user_data["id"], user_data["username"], "teacher")
    return None


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    bcrypt.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "user.login"

    app.register_blueprint(user_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(teacher_bp)

    return app
