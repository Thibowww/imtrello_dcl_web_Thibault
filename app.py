import flask
from flask import Flask, request
import datetime

from database.database import db, init_database
from projects import add_project, update_project

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../database/database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
with app.test_request_context():
    init_database()


@app.route('/')
def display_home_page():  # put application's code here
    return flask.render_template("welcome_page.html.jinja2")


@app.route('/login')
def display_login_page():
    return flask.render_template("login_page.html.jinja2")


@app.route('/register')
def display_register_page():
    return flask.render_template("register_page.html.jinja2")


@app.route('/myprojects')
def display_projects():
    return flask.render_template("my_projects.html.jinja2")


@app.route('/register', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def register_function():
    return


@app.route('/login', methods=['GET', 'POST'])
@app.route('/myprojects', methods=['GET', 'POST'])
def login_function():
    login_check, errors = login_checker(flask.request.form)
    if login_check:
        return display_projects()


def login_checker(form):
    login_check = True
    errors = ["id does not exist", "wrong password"]
    return login_check, errors


def create_project():
    name = request.form.get("name")
    description = request.form.get("description")
    deadline_str = request.form.get("deadline")  # Assuming the form sends a string representation of datetime

    # Check if name is provided
    if not name:
        return "Error: Project name is required"

    # Parse deadline string to datetime format
    deadline = None
    if deadline_str:
        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M:%S")  # Adjust format as needed
        except ValueError:
            return "Error: Invalid deadline format. Please use YYYY-MM-DD HH:MM:SS"

    add_project(name, description, deadline)
    return


def fonction_formulaire_create_project():
    form_est_valide, errors = formulaire_est_valide(flask.request.form)
    if not form_est_valide:
        return afficher_formulaire_create_project(flask.request.form, errors)
    else:
        return traitement_formulaire_create_project(flask.request.form)


def formulaire_est_valide(form):
    name = request.form.get("name")
    description = request.form.get("description")
    deadline_str = request.form.get("deadline")

    result = True
    errors = []

    if not name:
        errors += ["Error: Project name is required"]
        result = False

    if not description:
        errors += ["Error: Project description is required"]
        result = False

    if not deadline_str:
        errors += ["Error: Project deadline is required"]
        result = False

    return result, errors


def afficher_formulaire_create_project(form, errors):
    return flask.render_template("my_projects.html.jinja2", errors=errors)


def traitement_formulaire_create_project(form, errors):
    return


def modify_project(project_id):
    label = request.form.get("label")
    is_done = request.form.get("is_done")

    # Update the project using update_project function
    updated_project = update_project(project_id, label=label, is_done=is_done)

    return updated_project


if __name__ == '__main__':
    app.run()
