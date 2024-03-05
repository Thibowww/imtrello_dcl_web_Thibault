from . import db  # Assuming that the db instance is defined in the same directory

def init_database():
    db.create_all()
