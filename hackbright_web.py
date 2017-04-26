"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")



@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)
    project_list = hackbright.get_grades_by_github(github)

    html = render_template("student_info.html",
                            project_list=project_list,
                            first=first,
                            last=last,
                            github=github)

    return html

@app.route("/new-student")
def new_student_form():
    """Show form for creating a student."""

    return render_template("new_student.html")


@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student."""

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    github = request.form.get("github")

    hackbright.make_new_student(first_name, last_name, github)

    return render_template("add_confirmation.html", github=github)

@app.route("/student-info")
def show_student_info():
    """Show information for newly added student."""


    return render_template("student_info.html")

@app.route("/project")
def show_project_info():
    """Show information about a project."""

    project = request.args.get('project_title')

    project_title, description, max_grade = hackbright.get_project_by_title(project)

    return render_template("project_info.html",
                             project_title=project_title,
                             description=description,
                             max_grade=max_grade)



if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
