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
from app.validators import (
    validate_create_task,
    validate_login_user,
    validate_register_user,
    validate_update_task,
)
from app.exceptions import (
    TaskNotFoundError,
    AuthenticationError,
    AuthorizationError,
    DuplicateEmailError,
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
            raise AuthenticationError(
                "Authentication required."
            )
        validate_create_task(input)
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
        if current_user is None:
            raise AuthenticationError(
                "Authentication required."
        )
        validate_update_task(input)
        db_task = update_task(
            session=session,
            task_id=id,
            input=input,
            current_user=current_user,
        )
        return to_graphql_task(db_task)
    
    @strawberry.mutation
    def delete_task(
        self,
        id:int,
        info: strawberry.Info,
    ) -> DeleteTaskResponse:
        session = info.context.session
        current_user = info.context.user
        if current_user is None:
            raise AuthenticationError(
                "Authentication required."
        )
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
        input: RegisterUserInput,
        info: strawberry.Info,
    ) -> User | None:
        session = info.context.session
        validate_register_user(input)
        db_user = register_user(
            session=session,
            input=input,
        )
        return to_graphql_user(db_user)
        
    @strawberry.mutation
    def login(
        self,
        input: LoginInput,
        info: strawberry.Info,
    ) -> LoginResponse | None:
        session = info.context.session
        validate_login_user(input)
        return login_user(
            session=session,
            input=input,
        )