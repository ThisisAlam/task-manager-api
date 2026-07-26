from datetime import date, datetime

import strawberry

@strawberry.type
class Task:
    id:int
    title:str
    description:str
    status:str
    priority:str
    # using date import 
    due_date:date 
    # using datetime import
    created_at:datetime

@strawberry.input
class CreateTaskInput:
    title:str
    description:str
    status:str
    priority:str
    due_date:date 
    # graphql creates datetime automatically
    # created_at:datetime

@strawberry.input
class UpdateTaskInput:
    title:str
    description:str
    status:str
    priority:str
    due_date:date 

@strawberry.type
class DeleteTaskResponse:
    success:bool
    message:str 

@strawberry.type
class User:
    id:int
    username:str
    email:str

@strawberry.input
class RegisterUserInput:
    username:str
    email:str
    password:str

@strawberry.input
class LoginInput:
    email:str
    password:str

@strawberry.type
class LoginResponse:
    access_token:str
    token_type:str