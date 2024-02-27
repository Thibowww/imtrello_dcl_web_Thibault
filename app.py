import flask
from flask import Flask

from database.database import db, init_database

app = Flask(__name__)

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/database.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#
#
# db.init_app(app)
# with app.test_request_context():
#     init_database()


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


if __name__ == '__main__':
    app.run()
