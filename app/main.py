from fastapi import FastAPI
from .database import engine
#from . import models
from .routers import post, user, auth, vote
#from .config import settings
from fastapi.middleware.cors import CORSMiddleware
#models.Base.metadata.create_all(bind=engine) -> as we are using alembic we do not need to use this

app = FastAPI(
    root_path="/doc",
    servers=[
        {"url": "/redoc", "description": "ReDoc Documentation"},
        {"url": "/doc", "description": "Swagger UI Documentation"}
    ],
    docs_url="/",  # Swagger UI URL
    redoc_url="/redoc",  # ReDoc URL
    openapi_url="/openapi.json"
)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(post.router) # include everything post.router -> now fastapi will go to our routers folder to post and finds a match for a match
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)







