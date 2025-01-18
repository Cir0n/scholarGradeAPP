from app.extensions import bcrypt
from app.utils.database import Database
from config import Config

db = Database(vars(Config))


def create_user(username, password, role="student"):
    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    return db.create_user(username, password_hash, role)


def get_all_users():
    return db.get_user()
