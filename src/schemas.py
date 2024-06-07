from pydantic import BaseModel
from typing import Union


class PostCreate(BaseModel):
    title: str 
    text: Union[str, None] = None


class Post(PostCreate):
    id: int 
    user_id: int


class UserCreate(BaseModel):
    name: str


class User(UserCreate):
    id: int 
    posts: list[Post] = [] 
