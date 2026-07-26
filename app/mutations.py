import strawberry
from app.database import SessionLocal
from app.services import (
    create_task, 
    update_task,
    delete_task,
    register_user,
    login_user,
)
from app.graphql_types import (
    CreateTaskInput, 
    Task, 
    UpdateTaskInput,
    DeleteTaskResponse,
    User,
    RegisterUserInput,
    LoginInput,
    LoginResponse,
)
from app.mappers import (
    to_graphql_task, 
    to_graphql_user
)
from app.models import (
    TaskModel, 
    UserModel
)

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_task(
        self,
        input: CreateTaskInput,
        info: strawberry.Info,
    ) -> Task:
        session = info.context.session
        current_user = info.context.user
        if current_user is None:
            raise Exception(
                "Authentication required."
            )
        db_task = create_task(
            session=session,
            input=input,
            owner=current_user
        )
        return to_graphql_task(db_task)
    
    @strawberry.mutation
    def update_task(
        self,
        id: int,
        input: UpdateTaskInput,
        info: strawberry.Info,
    ) -> Task | None:
        session = info.context.session
        current_user = info.context.user
        try:
            db_task = update_task(
                session=session,
                task_id=id,
                input=input,
                current_user=current_user,
            )
            if db_task is None:
                return None
            return to_graphql_task(db_task)
        finally:
            session.close()

    @strawberry.mutation
    def delete_task(
        self,
        id:int,
        info: strawberry.Info,
    ) -> DeleteTaskResponse:
        session = info.context.session
        current_user = info.context.user
        deleted = delete_task(
            session=session,
            task_id=id,
            current_user=current_user,
        )
        if not deleted:
            return DeleteTaskResponse(
                success=False,
                message="Task not deleted",
            )
        return DeleteTaskResponse(
            success=True,
            message="Task deleted successfull",
        )

    @strawberry.mutation
    def register(
        self,
        input: RegisterUserInput
    ) -> User | None:
        session = SessionLocal()
        try:
            db_user= register_user(
                session=session,
                input=input,
            )
            if db_user is None:
                return None
            return to_graphql_user(db_user)
        finally:
            session.close()
    
    @strawberry.mutation
    def login(
        self,
        input: LoginInput,
    ) -> LoginResponse | None:
        session = SessionLocal()
        try:
            return login_user(
                session=session,
                input=input,
            )
        finally:
            session.close()