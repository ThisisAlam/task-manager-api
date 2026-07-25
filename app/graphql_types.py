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

@strawberry.type
class CreateTaskInput:
    title:str
    description:str
    status:str
    priority:str
    due_date:date 
    # graphql creates datetime automatically
    # created_at:datetime
@strawberry.type
class UpdateTaskInput:
    title:str
    description:str
    status:str
    priority:str
    due_date:date 