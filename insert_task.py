from datetime import date
from app.database import SessionLocal
from app.models import TaskModel

session = SessionLocal()
task = TaskModel(
    title="Learn fastAPI",
    description="Complete FastAPI Lesson",
    status="TODO",
    priority="HIGH",
    due_date=date(2026,8,15),
)
session.add(task)
session.commit()
print("Task inserted")
session.close()