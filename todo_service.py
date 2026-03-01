from datetime import datetime

tasks_db = []
task_id_counter = 1


def get_tasks():
    return {"tasks": tasks_db}


def add_task(title: str, description: str = "", due_date: str = None):
    global task_id_counter
    task = {
        "id": task_id_counter,
        "title": title,
        "description": description,
        "completed": False,
        "created_at": datetime.now().isoformat(),
        "due_date": due_date,
        "reminder_sent": False
    }
    tasks_db.append(task)
    task_id_counter += 1
    return {"success": True, "task": task}


def update_task(task_id: int, title: str = None, description: str = None, completed: bool = None, due_date: str = None):
    for task in tasks_db:
        if task["id"] == task_id:
            if title is not None:
                task["title"] = title
            if description is not None:
                task["description"] = description
            if completed is not None:
                task["completed"] = completed
            if due_date is not None:
                task["due_date"] = due_date
            return {"success": True, "task": task}
    return {"success": False, "error": "Task not found"}


def delete_task(task_id: int):
    global tasks_db
    for i, task in enumerate(tasks_db):
        if task["id"] == task_id:
            deleted_task = tasks_db.pop(i)
            return {"success": True, "task": deleted_task}
    return {"success": False, "error": "Task not found"}


def mark_reminder_sent(task_id: int):
    for task in tasks_db:
        if task["id"] == task_id:
            task["reminder_sent"] = True
            return True
    return False
