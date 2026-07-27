from datetime import date
from app.exceptions import ValidationError
from app.graphql_types import (
    CreateTaskInput,
    UpdateTaskInput,
    RegisterUserInput,
    LoginInput,
)
VALID_STATUSES = {
    "TODO",
    "IN_PROGRESS",
    "DONE",
}
VALID_PRIORITIES = {
    "LOW",
    "MEDIUM",
    "HIGH",
}

def _validate_task(input) -> None:
    if not input.title.strip():
        raise ValidationError("Title cannot be empty.")
    if not input.description.strip():
        raise ValidationError("Description cannot be empty.")
    if input.status not in VALID_STATUSES:
        raise ValidationError("Invalid task status.")
    if input.priority not in VALID_PRIORITIES:
        raise ValidationError("Invalid task priority.")
    if input.due_date < date.today():
        raise ValidationError("Due date cannot be in the past.")

def validate_create_task(input: CreateTaskInput) -> None:
    _validate_task(input)

def validate_update_task(input: UpdateTaskInput) -> None:
    _validate_task(input)

def validate_register_user(input: RegisterUserInput) -> None:
    if not input.username.strip():
        raise ValidationError("Username is required.")
    if len(input.username) < 3:
        raise ValidationError(
            "Username must be at least 3 characters."
        )
    if not input.email.strip():
        raise ValidationError("Email is required.")
    if "@" not in input.email:
        raise ValidationError("Invalid email address.")
    if not input.password:
        raise ValidationError("Password is required.")
    if len(input.password) < 8:
        raise ValidationError(
            "Password must be at least 8 characters."
        )

def validate_login_user(input: LoginInput) -> None:
    if not input.email.strip():
        raise ValidationError("Email is required.")
    if "@" not in input.email:
        raise ValidationError("Invalid email address.")
    if not input.password:
        raise ValidationError("Password is required.")

def validate_pagination(
    page: int,
    page_size: int,
) -> None:
    if page < 1:
        raise ValidationError(
            "Page must be at least 1."
        )
    if page_size < 1:
        raise ValidationError(
            "Page size must be at least 1."
        )
    if page_size > 100:
        raise ValidationError(
            "Page size cannot exceed 100."
        )