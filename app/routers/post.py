from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts'] # it groups the post function under posts in documention
)




# GET ALL POSTS
@router.get("/", response_model=List[schemas.PostOut]) # If we don’t use List[schemas.Post], FastAPI will expect the response to be a single post (matching the schemas.Post model) instead of a list of posts. Since our function returns a list of posts, the response structure won’t match the expected model, and FastAPI will throw an error.
def get_posts(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user), 
                limit: int = 10, skip: int = 0, search: Optional[str] = ""): # limit here is variable that we introduce so that user can tell how many queries should be return
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() 
    # to search "something like" in url you have to add percentage instead of space. http://ip.address/posts?search=something%like
    posts = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
            models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # here join is set to inner left join default but we want left outer join
    # label is used rename the column, like we use AS in sql
   
    return posts



# CREATE POST
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)): 
    # new_post = models.Post(title=post.title, content=post.content, published=post.published) -> one of the way but its quite limited
    print(current_user.id)
    new_post = models.Post(owner_id=current_user.id, **post.model_dump()) # here we use pydantic model (one we created above) as it matches our table schema, ** it will unpack the dictonary that we create using model_dump/dictonary
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # its an returning feature just like we do in sql
    return new_post



# GET ONE POST
@router.get("/{id}", response_model=schemas.PostOut) # prefix = "/posts" + /id
def get_post(id: int, db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)): 
    #post = db.query(models.Post).filter(models.Post.id == id).first() # do not do .all() it will throw an error as it will keep searching for similar id post even it has already found one post that matches the id
    post = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
            models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).first()
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} was not found")
    
    return post



# DELETE ONE POST
@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Post not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")
    
    post_query.delete(synchronize_session=False) # read the docs for the better explanation, generally its the most efficient and reliable once the session is expired
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# UPDATE ONE POST
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Post not found")
    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    updated_post = post_query.first()
    return updated_post
