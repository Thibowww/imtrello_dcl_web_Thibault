
import hashlib
from functools import wraps
import datetime
import flask
from flask import Flask, render_template, request, redirect, session, url_for

from manage_users import *
from database.database import db, init_database
from projects import add_project, update_project


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../database/database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


app.secret_key = 'imtrello'


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


def is_connected(f):
    @wraps(f)
    def fonction_decorateur(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("display_login_page"))
    return fonction_decorateur

@app.route('/myprojects')
@is_connected
def display_projects():
    return flask.render_template("my_projects.html.jinja2")


@app.route('/register', methods=['GET', 'POST'])
def register_function():
    donnees = request.form
    email = donnees.get("email")
    first_name = donnees.get("first_name")
    last_name = donnees.get("last_name")
    username = donnees.get("username")
    password = donnees.get("password")
    password_confirm = donnees.get("password_confirm")
    register_check, errors_data, errors_password = register_checker(email, username, password, password_confirm)
    if register_check:
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password1 = hash.hexdigest()
        create_user(first_name, last_name, email, username, password1)
        return display_login_page()
    else:
        return display_home_page()

def register_checker(email, username, password, password_confirm):
    '''
    vérifier que les mots de passe correspondent
    vérifier qu'ils respectent certains critères
    vérifier que l'username ou l'email n'existe pas déjà
    '''
    register_check=True
    errors_data = register_check_data(email, username)
    print(errors_data)
    password_error = []
    if password != password_confirm:
        password_error.append("Passwords don't match")
        register_check=False
    print(register_check)
    if len(password)<8:
        password_error.append("Password too short, use at least 8 caracteres")
        register_check = False
    print(register_check)
    if len(errors_data)!=0:
        register_check=False
    print(register_check)
    return register_check, errors_data, password_error


@app.route('/login', methods=['GET', 'POST'])
@app.route('/myprojects', methods=['GET', 'POST'])
def login_function():
    donnees = request.form
    username = donnees.get("username")
    password = donnees.get("password")
    login_check, error = login_checker(username, password)
    if login_check:
        session['username'] = username
        return display_projects()
    else:
        return display_login_page()

def login_checker(username, password):
    login_check = False
    hash = password + app.secret_key
    hash = hashlib.sha1(hash.encode())
    password = hash.hexdigest()
    if check_password(username, password):
        error = None
        login_check=True
        return login_check, error
    error="User doesn't exist or wrong password"
    return login_check, error

@app.route('/home_page', methods=['GET', 'POST'])

def logout_function():
    session.pop('username', None)
    return display_home_page()



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
