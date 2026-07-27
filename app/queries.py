import strawberry
from typing import List
from datetime import date, datetime, UTC
from app.graphql_types import (
    Task,
    User,
    TaskSortField,
    SortOrder,
)
from app.mappers import (
    to_graphql_task, 
    to_graphql_user,
)
from app.database import SessionLocal
from app.services import (
    get_task_by_id, 
    get_tasks
)
from graphql import GraphQLError
from app.validators import validate_pagination

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
    def tasks(
        self,
        info: strawberry.Info,
        page: int= 1,
        page_size: int= 10,
        status: str|None=None,
        priority: str|None=None,
        search: str|None=None,
        sort_by: TaskSortField = TaskSortField.CREATED_AT,
        order: SortOrder = SortOrder.DESC
    )->List[Task] | None:
        validate_pagination(
            page=page,
            page_size=page_size,
        )
        session = info.context.session 
        db_task=get_tasks(
            session=session,
            page=page,
            page_size=page_size,
            status=status,
            priority=priority,
            search=search,
            sort_by=sort_by,
            order=order,
        )
        if db_task is None:
            return None
        return [
            to_graphql_task(task)
            for task in db_task
        ]

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
   