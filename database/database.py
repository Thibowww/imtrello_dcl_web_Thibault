from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_database():
    db.create_all()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.Text)
    isDone = db.Column(db.Boolean)

