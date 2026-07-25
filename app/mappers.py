from app.models import TaskModel
from app.graphql_types import Task

def to_graphql_task(db_task:TaskModel)->Task:
    return Task(
        id=db_task.id,
        title=db_task.title,
        description=db_task.description,
        status=db_task.status,
        priority=db_task.priority,
        due_date=db_task.due_date,
        created_at=db_task.created_at,
    )
