from app.extensions import bcrypt
from app.services.student_service import (create_student,
                                          get_student_by_username)
from app.services.teacher_service import (create_teacher,
                                          get_teacher_by_username)
from app.utils.database import Database
from config import Config

db = Database(vars(Config))


def validate_user_registration_data(username, password, role="student"):
    if not username or not password:
        return {"ERROR": "Nom d'utilisateur et mot de passe requis"}
    if role not in ["student", "teacher"]:
        return {"ERROR": "Rôle invalide"}
    return None


def is_username_available(username):
    student = get_student_by_username(username)
    teacher = get_teacher_by_username(username)
    return student is None and teacher is None


def create_user(
    first_name, last_name, username, password, role, extra_data=None
):
    validation_error = validate_user_registration_data(
        username, password, role
    )
    if validation_error:
        return validation_error

    if not is_username_available(username):
        return {"error": "Nom d'utilisateur déjà pris"}

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    if role == "student":
        result = create_student(
            first_name, last_name, username, password_hash, extra_data
        )
    elif role == "teacher":
        result = create_teacher(
            first_name, last_name, username, password_hash, extra_data
        )
    else:
        result = "ERROR"
    return result


def verify_user_credentials(username, password):
    user = get_student_by_username(username) or get_teacher_by_username(
        username
    )

    if not user or not bcrypt.check_password_hash(user["password"], password):
        return {"error": "Nom d'utilisateur ou mot de passe incorrect"}

    user["role"] = "student" if "class" in user else "teacher"
    return {"data": user}
