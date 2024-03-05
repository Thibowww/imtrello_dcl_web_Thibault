from .models import Task
from . import db  # Assuming that the db instance is defined in the same directory

def init_database():
    db.create_all()

def add_task(label, is_done=False):
    new_task = Task(label=label, isDone=is_done)
    db.session.add(new_task)
    db.session.commit()
    return new_task

def get_all_tasks():
    return Task.query.all()

def get_task_by_id(task_id):
    return Task.query.get(task_id)  # Retrieve task by its primary key (id)

def get_task_by_label(label):
    return Task.query.filter_by(label=label).first()  # Retrieve task by label

def get_all_tasks_by_label(label):
    return Task.query.filter_by(label=label).all()  # Retrieve all tasks with given label

def update_task(task_id, label=None, is_done=None):
    task = Task.query.get(task_id)
    if task:
        if label is not None:
            task.label = label
        if is_done is not None:
            task.isDone = is_done
        db.session.commit()
    return task

def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return task

def delete_all_tasks():
    deleted_tasks = Task.query.delete()
    db.session.commit()
    return deleted_tasks


def get_tasks_by_status(is_done):
    return Task.query.filter_by(isDone=is_done).all()

def get_total_tasks():
    return Task.query.count()

def get_all_tasks_sorted_by_label():
    return Task.query.order_by(Task.label).all()

def search_tasks_by_keyword(keyword):
    return Task.query.filter(Task.label.ilike(f'%{keyword}%')).all()