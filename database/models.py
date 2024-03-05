from database.database import db


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Boolean)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)


user_to_project = db.Table('user to project',
                           db.Column("project_id", db.Integer, db.ForeignKey('team.id')),
                           db.Column("user_id", db.Integer, db.ForeignKey('user.id')),
                           )


class Project(db.Model):
    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.Text)
