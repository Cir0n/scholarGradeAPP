from config import Config
from app.utils.database import Database

db = Database(vars(Config))

def create_teacher(first_name, last_name, username, password, subject):
    if not username or not subject:
        return {"error": "Nom d'utilisateur et matière requis"}

    existing_teacher = db.get_teacher_by_username(username)
    if existing_teacher:
        return {"error": "Nom d'utilisateur déjà pris"}

    db.create_teacher(first_name, last_name, username, password, subject)
    return {"message": "Enseignant créé avec succès"}


def get_all_teachers():
    teachers = db.get_all_teachers()
    return teachers

def get_teacher_by_id(teacher_id):
    teacher = db.get_teacher_by_id(teacher_id)
    return teacher

def get_teacher_by_username(username):
    teacher = db.get_teacher_by_username(username)
    return teacher


def add_grade_for_student(student_id, subject, grade, comment=None):
    if not student_id or not subject or grade is None:
        return {"error": "Données manquantes pour ajouter une note"}

    db.add_grade(student_id, subject, grade, comment)
    return {"message": "Note ajoutée avec succès"}
