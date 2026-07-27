from sqlalchemy import or_
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
    TaskSortField,
    SortOrder
)
from app.security import (
    hash_password, 
    verify_password
)
from app.exceptions import (
    TaskNotFoundError,
    AuthenticationError,
    AuthorizationError,
    DuplicateEmailError,
)
from app.jwt_handler import create_access_token

def get_task_by_id(
    session:Session,
    task_id:int
):
    query = session.get(TaskModel, task_id)
    if query is None:
        raise TaskNotFoundError("Task not found.")
    return query

def get_tasks(
    session:Session,
    page:int,
    page_size:int,
    status: str | None=None,
    priority:str | None=None,
    search: str | None=None,
    sort_by: TaskSortField = TaskSortField.CREATED_AT,
    order: SortOrder = SortOrder.DESC,
):
    offset = (page - 1) * page_size
    query = session.query(TaskModel)
    if status:
        query = query.filter(TaskModel.status == status)
    if priority:
        query = query.filter(TaskModel.priority == priority)
    if search:
        query = query.filter(
            or_(
                TaskModel.title.ilike(f"%{search}%"),
                TaskModel.description.ilike(f"%{search}%"),
            )
        )
    sort_columns = {
        TaskSortField.CREATED_AT: TaskModel.created_at,
        TaskSortField.DUE_DATE: TaskModel.due_date,
        TaskSortField.TITLE: TaskModel.title,
    }
    column = sort_columns[sort_by]
    if order == SortOrder.ASC:
        query = query.order_by(column.asc())
    else:
        query = query.order_by(column.desc())

    return (
        query
        .offset(offset)
        .limit(page_size)
        .all()
    )

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
        raise TaskNotFoundError("Task not found.")
    if task.owner_id != current_user.id:
        raise AuthorizationError("Not authorized.")
        # Exception(
        #     "Not authorized."
        # )
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
        raise AuthorizationError("Not authorized.")
        # Exception(
        #     "Not authorized."
        # )
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
        raise AuthenticationError("Invalid email or password.")
    if not verify_password(
        input.password,
        user.password,
    ):
        raise AuthenticationError("Invalid Email and Password.")
    token = create_access_token(user.id)
    return LoginResponse(
        access_token=token,
        token_type="Bearer",
    )
