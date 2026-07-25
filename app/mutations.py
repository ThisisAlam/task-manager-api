import strawberry
from app.database import SessionLocal
from app.services import (
    create_task, 
    update_task,
    delete_task,
)
from app.graphql_types import (
    CreateTaskInput, 
    Task, 
    UpdateTaskInput,
    DeleteTaskResponse,    
)
from app.mappers import to_graphql_task
from app.models import TaskModel

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_task(
        self,
        input: CreateTaskInput,
    ) -> Task:
        session = SessionLocal()
        try:
            db_task = create_task(
                session,
                input,
            )
            return to_graphql_task(db_task)
        finally:
            session.close()
    
    @strawberry.mutation
    def update_task(
        self,
        id:int,
        input: UpdateTaskInput,
    ) -> Task | None:
        session = SessionLocal()
        try:
            db_task = update_task(
                session=session,
                task_id=id,
                input=input,
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
    ) -> DeleteTaskResponse:
        session = SessionLocal()
        try:
            deleted = delete_task(
                session=session,
                task_id=id,
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
        finally:
            session.close()