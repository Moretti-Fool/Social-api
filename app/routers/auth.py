from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from .. import schemas, models, utils, oauth2


router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # in OAuth2PasswordRequestForm it has username and password field not email, so we just need to use user_credentials.username instead of user.credentials.email, it doesnt really matter
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user_credentials.username or not user_credentials.password:
        raise HTTPException(status_code=422, detail="Missing required fields")
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentails")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    
    #create a token
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    #return token
    return {"access_token": access_token, "token_type": "bearer"}
    # remember while testing this using postman use body -> form-data instead of body -> raw
