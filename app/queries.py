import strawberry
from typing import List
from datetime import date, datetime, UTC
from app.graphql_types import Task
from app.mappers import to_graphql_task
from app.database import SessionLocal
from app.services import get_task_by_id, get_all_tasks
@strawberry.type
class Query:
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