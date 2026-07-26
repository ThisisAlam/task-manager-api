import strawberry
from typing import List
from datetime import date, datetime, UTC
from app.graphql_types import (
    Task,
    User,
)
from app.mappers import (
    to_graphql_task, 
    to_graphql_user,
)
from app.database import SessionLocal
from app.services import (
    get_task_by_id, 
    get_all_tasks
)
from graphql import GraphQLError

@strawberry.type
class Query:

    @strawberry.field
    def me(
        self,
        info: strawberry.Info,
    ) -> User:
        current_user = info.context.user
        if current_user is None:
            raise GraphQLError(
                "Authentication required."
            )
        return to_graphql_user(current_user)

    @strawberry.field
    def tasks(self)->List[Task]|None:
        session=SessionLocal()
        try:
            db_task=get_all_tasks(session)
            if db_task is None:
                return None
            return [
                to_graphql_task(task)
                for task in db_task
            ]
        finally:
            session.close()

    @strawberry.field
    def task(self, id:int) -> Task|None:
        session=SessionLocal()
        try:
            db_task=get_task_by_id(session,id)
            if db_task is None:
                return None
            return to_graphql_task(db_task)
        finally:
            session.close()
   