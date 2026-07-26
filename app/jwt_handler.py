from datetime import datetime, timedelta,UTC, timezone
import jwt
from app.settings import settings

def create_access_token(user_id:int)->str:
    payload={
        "sub":str(user_id),
        "exp":datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    }
    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def verify_access_token(token:str):
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )