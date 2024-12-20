from fastapi import  APIRouter
from pydantic import BaseModel, Field, EmailStr
from user_jwt import create_token

routerUser= APIRouter()


class User(BaseModel):
    
    email:EmailStr | None = Field(default=None)
    password: str 
    


@routerUser.post('/login', status_code=201, tags=['Auth'])
def login(user:User):
    token: str = create_token(user.model_dump())
    return {'acces_token':token, 'result':'ok'}
