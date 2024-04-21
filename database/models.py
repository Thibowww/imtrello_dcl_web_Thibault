from database.database import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.Text)
    isDone = db.Column(db.Boolean)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    deadline = db.Column(db.DateTime)

    # Define a relationship with the Project model
    project = db.relationship('Project', backref=db.backref('tasks', lazy=True))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    comment = db.Column(db.Text)
    task = db.relationship('Task', backref=db.backref('comments', lazy=True))

user_to_project = db.Table('user_to_project',
                           db.Column("project_id", db.Integer, db.ForeignKey('project.id')),
                           db.Column("user_id", db.Integer, db.ForeignKey('user.id')),
                           )

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Integer)
    message = db.Column(db.String(255))
    lu = db.Column(db.Boolean)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    project = db.relationship('Project', backref=db.backref('notifs', lazy=True))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.Text)
    manager = db.Column(db.Text)
    users = db.relationship('User', backref='projects', secondary=user_to_project)  # Project <-> User relationship
    description = db.Column(db.Text)
    deadline = db.Column(db.DateTime)
    isDone = db.Column(db.Boolean)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    email = db.Column(db.Text)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
