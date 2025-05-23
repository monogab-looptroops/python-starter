from fastapi import APIRouter
from loggerhelper import LoggerHelper, LogLevel


from api.models import User

#
# This is an example router
# This can be used like a boilerplate for creating new routers
#


logger = LoggerHelper(__name__, log_level=LogLevel.INFO)


router_example = APIRouter()
tags = ['router example']

@router_example.get("/hello/world",tags=tags)
def hello_world():
    """
        Dummy endpoint to test the router
    """
    return {"Hello": "World"}


@router_example.get("/api/{user_id}",tags=tags) 
def get_user(user_id:int) -> User:
    """
        Dummy endpoint with User model
    """
    return User( id = user_id, name = "John", dob = "1990-01-01")
   







