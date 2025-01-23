from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>:<port>/<database_name>
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL) # connect to database

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # some default 

Base = declarative_base() # models that we are going to define will be extended from this class


# Dependency   ->  it gets a connection/session to our database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()