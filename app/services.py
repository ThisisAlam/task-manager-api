from app.models import TaskModel
from app.graphql_types import (
    CreateTaskInput, 
    UpdateTaskInput,
    DeleteTaskResponse,
)
from sqlalchemy.orm import Session

def get_task_by_id(
    session:Session,
    task_id:int
):
    query = session.get(TaskModel, task_id)
    return query

def get_all_tasks(
    session:Session
):
    query = session.query(TaskModel).all()
    return query

def create_task(
    session:Session,
    input:CreateTaskInput,
):
    task = TaskModel(
        title=input.title,
        description=input.description,
        status=input.status,
        priority=input.priority,
        due_date=input.due_date,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def update_task(
    session:Session,
    task_id:int,
    input:UpdateTaskInput,
):
    task = get_task_by_id(session,task_id)
    if task is None:
        return None
    task.title=input.title
    task.description=input.description
    task.status=input.status
    task.priority=input.priority
    task.due_date=input.due_date
    session.commit()
    session.refresh(task)
    return task
def delete_task(
    session:Session,
    task_id:int,
):
    task=get_task_by_id(session,task_id)
    if task is None:
        return False
    session.delete(task)
    session.commit()
    return True