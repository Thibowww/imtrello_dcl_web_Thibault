from . import db  # Assuming that the db instance is defined in the same directory
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def init_database():
    db.create_all()

