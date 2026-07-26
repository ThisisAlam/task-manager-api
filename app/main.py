from fastapi import FastAPI, Request
from strawberry.fastapi import GraphQLRouter
from app.context import Context
from app.schema import schema
from app.jwt_handler import verify_access_token
from app.database import SessionLocal
from app.services import get_user_by_id

app=FastAPI()
async def get_context(request:Request):
    session=SessionLocal()
    try: 
        current_user=None
        authorization = request.headers.get("Authorization")
        if authorization:
            token= authorization.replace("Bearer ", "")
            payload= verify_access_token(token)
            current_user= get_user_by_id(
                session,
                int(payload["sub"])
            )
        return Context(
            session=session,
            user=current_user,
        )
    finally:
        session.close()


graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context,
)

app.include_router(
    graphql_app,
    prefix="/graphql",
)

@app.get("/")
def root():
    return {
        "message":"Task manager api from address /"
    }