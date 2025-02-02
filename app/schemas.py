from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True # its an optional value, and its default value is set to True, user can change it they want to
    

class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime



class Post(PostBase): # Response Schema , we dont need to mention title,content,published as it inherits from Postbase class, we only need to specify new columns
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    #class Config:    we dont need that, maybe because video is old and pydantic or database has added new feature about this? as in video he said that as we refresh(new_post) it do not converts the new_post into dictonary and pydantic models deals with dictonary thats why it was giving an error
        #orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str




class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
    

class Vote(BaseModel):
    post_id: int
    dir: int #less than equal to 1

