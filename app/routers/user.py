from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)



# USER REGISTRATION
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, 
                      db: Session = Depends(get_db)):
    if user.password != user.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match."
        )
    
    # Check if the email already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered."
        )
    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password


    new_user = models.User(
        email=user.email,
        password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user



# GET LOGGED IN USERS POSTS
@router.get("/myposts", response_model=List[schemas.Post]) # If we don’t use List[schemas.Post], FastAPI will expect the response to be a single post (matching the schemas.Post model) instead of a list of posts. Since our function returns a list of posts, the response structure won’t match the expected model, and FastAPI will throw an error.
def get_posts(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() # grabs every row in the table
    
    return posts

# FETCH USER DETAILS
@router.get("/details", response_model=schemas.UserOut)
def get_user(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} does not exists")
    
    return user




