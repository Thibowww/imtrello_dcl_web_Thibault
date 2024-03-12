import hashlib
from functools import wraps

import flask
from flask import Flask, render_template, request, redirect, session, url_for

from manage_users import *
from database.database import db, init_database


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



if __name__ == '__main__':
    app.run()
