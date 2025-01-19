from flask import Blueprint, render_template
from flask_login import current_user, login_required

from app.services.student_service import get_student_grades

student_bp = Blueprint("student", __name__)


@student_bp.route("/student/grades", methods=["GET"])
@login_required
def view_grades():
    if current_user.role != "student":
        return "Unauthorized", 403
    grades = get_student_grades(current_user.id)
    return render_template("student_grades.html", grades=grades)


