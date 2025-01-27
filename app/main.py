from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.requests import Request
#from .database import engine
#from . import models
from .routers import post, user, auth, vote
#from .config import settings
from fastapi.middleware.cors import CORSMiddleware
#models.Base.metadata.create_all(bind=engine) -> as we are using alembic we do not need to use this

app = FastAPI(

    redoc_url="/redoc",
    docs_url="/doc",
    openapi_url="/openapi.json"
)

templates = Jinja2Templates(directory="app/templates")
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



# Route to serve the index page
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Route to Swagger UI
@app.get("/doc")
async def custom_docs():
    return RedirectResponse(url="/swagger")

# Route to ReDoc
@app.get("/redoc")
async def custom_redoc():
    return RedirectResponse(url="/redoc")