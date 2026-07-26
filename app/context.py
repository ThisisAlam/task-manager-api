from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session
from strawberry.fastapi import BaseContext

from app.models import UserModel

@dataclass
class Context(BaseContext):
    session: Session
    user: Optional[UserModel] = None