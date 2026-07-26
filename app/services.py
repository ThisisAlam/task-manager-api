from sqlalchemy.orm import Session
from app.models import (
    TaskModel, 
    UserModel
)
from app.graphql_types import (
    CreateTaskInput, 
    UpdateTaskInput,
    DeleteTaskResponse,
    RegisterUserInput,
    LoginInput,
    LoginResponse,
    Task,
    User,
)
from app.security import (
    hash_password, 
    verify_password
)
from app.jwt_handler import create_access_token

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

def get_user_by_id(
    session:Session,
    user_id:str
)->User:
    query=(
        session.get(UserModel,user_id)
    )
    return query
def get_user_by_email(
    session:Session,
    email:str
)->User:
    query=(
        session.query(UserModel)
        .filter(UserModel.email==email)
        .first()
    )
    return query


def create_task(
    session:Session,
    input:CreateTaskInput,
    owner,
):
    task = TaskModel(
        title=input.title,
        description=input.description,
        status=input.status,
        priority=input.priority,
        due_date=input.due_date,
        owner_id=owner.id,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def update_task(
    session:Session,
    task_id:int,
    input:UpdateTaskInput,
    current_user,
):
    task = get_task_by_id(session,task_id)
    if task is None:
        return None
    if task.owner_id != current_user.id:
        raise Exception(
            "Not authorized."
        )
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
    current_user,
):
    task=get_task_by_id(session,task_id)
    if task is None:
        return False
    if task.owner_id != current_user.id:
        raise Exception(
            "Not authorized."
        )
    session.delete(task)
    session.commit()
    return True

def register_user(
    session:Session,
    input:RegisterUserInput,
):
    user=UserModel(
        username=input.username,
        email=input.email,
        password=hash_password(input.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def login_user(
    session:Session,
    input:LoginInput,
):
    user=get_user_by_email(
        session,
        input.email
    )
    if user is None:
        return None
    if not verify_password(
        input.password,
        user.password,
    ):
        return None
    token = create_access_token(user.id)
    return LoginResponse(
        access_token=token,
        token_type="Bearer",
    )
