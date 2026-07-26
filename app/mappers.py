from app.models import TaskModel, UserModel
from app.graphql_types import Task, User
from app.security import hash_password

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

def to_graphql_user(db_user: UserModel) -> User:
    return User(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
    )