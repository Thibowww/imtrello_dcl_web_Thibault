from database.models import User, Project
from database.database import db, init_database


def create_user(username, password):
    new_user = User(username=username, password=password)


def create_project():
    new_project = Project()