from database.models import Task, Project
from database.database import db


# Functions to manage tasks within projects
def add_task_to_project(project_id, label, is_done=False):
    """Add a new task to a project."""
    project = Project.query.get(project_id)
    if project:
        new_task = Task(label=label, isDone=is_done, project_id=project_id)
        db.session.add(new_task)
        db.session.commit()
        return new_task
    return None


def get_tasks_in_project(project_id):
    """Retrieve all tasks within a project."""
    project = Project.query.get(project_id)
    if project:
        return project.tasks
    return []


def update_task_in_project(task_id, label=None, is_done=None):
    """Update a task within a project."""
    task = Task.query.get(task_id)
    if task:
        if label is not None:
            task.label = label
        if is_done is not None:
            task.isDone = is_done
        db.session.commit()
    return task


def delete_task_from_project(task_id):
    """Delete a task from a project."""
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return task


def add_project(project_name, description, deadline):
    new_project = Project(project_name=project_name, users=[], description=description, deadline=deadline, isDone=False)
    db.session.add(new_project)
    db.session.commit()
    return new_project


def get_all_projects():
    """Retrieve all projects from the database."""
    return Project.query.all()


def get_project_by_id(project_id):
    """Retrieve a project by its ID."""
    return Project.query.get(project_id)


def update_project(project_id, label=None, is_done=None):
    """Update a project's label and/or isDone status."""
    project = Project.query.get(project_id)
    if project:
        if label is not None:
            project.label = label
        if is_done is not None:
            project.isDone = is_done
        db.session.commit()
    return project


def delete_project(project_id):
    """Delete a project by its ID."""
    project = Project.query.get(project_id)
    if project:
        db.session.delete(project)
        db.session.commit()
    return project


def delete_all_projects():
    """Delete all projects from the database."""
    deleted_projects = Project.query.delete()
    db.session.commit()
    return deleted_projects


def get_projects_by_status(is_done):
    """Retrieve projects based on their status (done or not done)."""
    return Project.query.filter_by(isDone=is_done).all()


def get_total_projects():
    """Retrieve the total number of projects in the database."""
    return Project.query.count()


def get_all_projects_sorted_by_label():
    """Retrieve all projects sorted alphabetically by their label."""
    return Project.query.order_by(Project.label).all()


def search_projects_by_keyword(keyword):
    """Search for projects containing a specific keyword in their label."""
    return Project.query.filter(Project.label.ilike(f'%{keyword}%')).all()
