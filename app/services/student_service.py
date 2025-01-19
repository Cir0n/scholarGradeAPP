from app.extensions import bcrypt
from config import Config
from app.utils.database import Database

db = Database(vars(Config))


def create_student(first_name, last_name, username, password, student_class):
    if not username or not password:
        return {"error": "Nom d'utilisateur et mot de passe requis"}

    existing_student = db.get_student_by_username(username)
    if existing_student:
        return {"error": "Nom d'utilisateur déjà pris"}

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    db.create_student(
        first_name, last_name, username, password_hash, student_class
    )
    return {"message": "Étudiant créé avec succès"}


def get_all_students():
    students = db.get_all_students()
    return students

def get_student_by_id(student_id):
    student = db.get_student_by_id(student_id)
    return student


def get_student_by_username(username):
    student = db.get_student_by_username(username)
    return student


def get_student_grades(student_id):
    grades = db.get_student_grade(student_id)
    return grades


def find_student_by_name(first_name, last_name):
    student = db.fetch_one(
        "SELECT id FROM students WHERE first_name = %s AND last_name = %s",
        (first_name, last_name),
    )
    return student
