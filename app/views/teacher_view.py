from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.teacher_service import add_grade_for_student
from app.services.student_service import find_student_by_name

teacher_bp = Blueprint("teacher", __name__)

@teacher_bp.route("/add-grade", methods=["GET", "POST"])
@login_required
def add_grade():
    if current_user.role != "teacher":
        print(current_user.username)
        return "Unauthorized", 403

    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        subject = request.form.get("subject")
        grade = request.form.get("grade")
        comment = request.form.get("comment")

        student = find_student_by_name(first_name, last_name)
        if "error" in student:
            flash(student["error"], "danger")
            return render_template("add_grade.html")

        student_id = student["data"]["id"]
        response = add_grade_for_student(student_id, subject, grade, comment)
        if "error" in response:
            flash(response["error"], "danger")
        else:
            flash("Note ajoutée avec succès.", "success")
            return redirect("/add-grade")

    return render_template("add_grade.html")
