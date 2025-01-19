from app.extensions import bcrypt
from app.utils.database import Database
from config import Config

db = Database(vars(Config))


def get_all_users():
    return db.get__all_user()

def get_user_by_username(username):
    return db.get_user_by_username(username)

def get_user_by_id(user_id):
    return db.get_user_by_id(user_id)

def validate_user_data(username, password, role="student"):
    if not username or not password:
        return {"error": "Nom d'utilisateur et mot de passe requis"}, False
    if role not in ["student", "teacher"]:
        return {"error": "Rôle invalide"}, False
    return None, True

def is_username_available(username):
    user = get_user_by_username(username)
    return user is None

def create_user(username, password, role="student"):
    validation, is_valid = validate_user_data(username, password, role)

    if not is_valid:
        return validation, False
    if not is_username_available(username):
        return {"error": "Nom d'utilisateur déjà pris"}, False
    
    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    return db.create_user(username, password_hash, role), True
    

