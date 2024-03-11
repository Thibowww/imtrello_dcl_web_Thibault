from database.database import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.Text)
    isDone = db.Column(db.Boolean)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    # Define a relationship with the Project model
    project = db.relationship('Project', backref=db.backref('tasks', lazy=True))


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.Text)
    description = db.Column(db.Text)
    deadline= db.Column(db.DateTime)
    isDone = db.Column(db.Boolean)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.Text)
    isDone = db.Column(db.Boolean)
