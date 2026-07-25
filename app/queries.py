import strawberry
from datetime import date, datetime, UTC
from app.graphql_types import Task

@strawberry.type
class Query:
    @strawberry.field
    def example_task(self) -> Task:
        return Task(
            id=1,
            title="Learn GraphQL",
            description="Complete Lesson 5",
            status="TODO",
            priority="HIGH",
            due_date=date(2026, 8, 15),
            created_at=datetime.utcnow(),
        )