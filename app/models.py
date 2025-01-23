from .database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text



class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE") ,nullable=False) 
    
    # RELATIONSHIP - automatically fetches that data for us so that we dont have to manually do it ourselves
    owner = relationship("User") # here "User" is the class 

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True,nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Votes(Base):
    __tablename__ = 'votes'
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete="CASCADE"),primary_key=True)


'''
Limitations of sqlalchemy -> {
   if we do any changes/modifications/migrations like changing in the column schema (eg adding new attribute or modify an attribute) in table class after it has been made, 
        it will not apply those modification if we save it or rerun the application.
    thats why we need to those another library - alembic
}
'''



    
    