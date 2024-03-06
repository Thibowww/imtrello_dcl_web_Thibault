from database.database import db


user_to_project = db.Table('user_to_project',
                           db.Column("project_id", db.Integer, db.ForeignKey('project.id')),
                           db.Column("user_id", db.Integer, db.ForeignKey('user.id')),
                           )


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.Text)
    users = db.relationship('User', backref='projects', secondary=user_to_project)  # Sport <-> Player relationship


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    email = db.Column(db.Text)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
