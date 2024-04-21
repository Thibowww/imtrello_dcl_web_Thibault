from database.models import Task, Project, User, user_to_project, Comment, Notification
from database.database import db


# Functions to manage tasks within projects
def add_task_to_project(project_id, task_name, deadline, is_done=False):
    project = Project.query.get(project_id)
    if project:
        new_task = Task(task_name=task_name,deadline=deadline, isDone=is_done, project_id=project_id)
        db.session.add(new_task)
        db.session.commit()
        developers = []
        for user in project.users:
            developers.append(user.username)
        message = "Une tâche a été ajouté une tâche au projet " + project.project_name + ""
        if developers is not None:
            add_notif(developers, message, project.id)
        return new_task
    return None

def add_comment_to_task(task_id, comment):
    task = Task.query.get(task_id)
    if task:
        new_comment = Comment(comment=comment, task_id=task_id)
        db.session.add(new_comment)
        db.session.commit()
        project = Project.query.filter_by(id=task.project_id).first()
        developers = []
        for user in project.users:
            if user.username != project.manager:
                developers.append(user.username)
        message = " Un commentaire a été ajouté à la tâche " + task.task_name + " du projet " + project.project_name + ""
        if developers is not None:
            add_notif(developers, message, project.id)
        db.session.commit()
        return new_comment
    return None


def get_tasks_in_project(project_id):
    project = Project.query.get(project_id)
    if project:
        return project.tasks
    return []

def get_comment_in_task(task_id):
    task = Task.query.get(task_id)
    if task:
        return task.comments
    return []
def get_task_by_id(task_id):
    task = Task.query.get(task_id)
    return task


def update_task_in_project(task_id, task_name,
                                   deadline):
    task = Task.query.get(task_id)
    if task:
        if task_name is not None:
            task.task_name = task_name
        if deadline is not None:
            task.deadline = deadline
        project= Project.query.filter_by(id=task.project_id).first()
        developers = []
        for user in project.users:
            if user.username != project.manager:
                developers.append(user.username)
        message = project.manager + " a modifier la tâche "+task.task_name+" du projet " + project.project_name + ""
        if developers is not None:
            add_notif(developers, message, project.id)
        db.session.commit()
    return task


def delete_task_from_project(task_id):
    task = Task.query.get(task_id)
    if task:
        comments = Comment.query.filter_by(task_id=task_id).all()
        for comment in comments:
            db.session.delete(comment)
        db.session.delete(task)
        db.session.commit()
        project = Project.query.filter_by(id=task.project_id).first()
        developers = []
        for user in project.users:
            if user.username != project.manager:
                developers.append(user.username)
        message = project.manager + " a supprimé la tache "+task.task_name+" du project " + project.project_name + ""
        if developers is not None:
            add_notif(developers, message, project.id)
    return task


def add_project(developers, project_name, description, deadline, manager_name):

    new_project = Project(project_name=project_name, manager=manager_name, description=description, deadline=deadline, isDone=False)
    db.session.add(new_project)
    db.session.commit()
    new_project.users.append(User.query.filter_by(username=manager_name).first())
    if developers is not None:
        for user in developers:
            if User.query.filter_by(username=user).first():
                new_project.users.append(User.query.filter_by(username=user).first())
    db.session.commit()
    message = manager_name+" vous a ajouté au projet "+ project_name+""
    if developers is not None:
        add_notif(developers, message, new_project.id)
    return new_project


def add_notif(users, message, project_id):
    for user in users:
        new_notif = Notification(username=user, message=message, project_id=project_id, lu=False)
        db.session.add(new_notif)
    db.session.commit()

def get_notif_by_user(username):
    return Notification.query.filter_by(username=username).all()
def update_project_in_database(project_id, developers, project_name=None, description=None, deadline=None, is_done=None):
    project = db.session.query(Project).get(project_id)
    message = project.manager + " a modifié le projet " + project_name + ""
    if project:
        if project_name is not None:
            project.project_name = project_name
        if description is not None:
            project.description = description
        if deadline is not None:
            project.deadline = deadline
        if is_done is not None:
            project.isDone = is_done
        if developers is not None:
            for user in developers:
                project.users.append(User.query.filter_by(username=user).first())
            message = project.manager + " vous a ajouté au projet " + project_name + ""
        db.session.commit()

        if developers is not None:
            add_notif(developers, message, project.id)
    return project


def get_all_projects(username):
    projects = Project.query.join(user_to_project).join(User).filter(User.username == username).all()
    return projects


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


def delete_project_in_database(project_id):
    """Delete a project by its ID."""
    project = Project.query.get(project_id)
    if project:
        tasks = Task.query.filter_by(project_id=project_id).all()
        if tasks :
            for task in tasks:
                db.session.delete(task)
        notifs = Notification.query.filter_by(project_id=project_id).all()
        if notifs :
            for notif in notifs:
                db.session.delete(notif)
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

