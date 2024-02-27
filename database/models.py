from database.database import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.Text)
    isDone = db.Column(db.Boolean)
