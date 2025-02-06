# all of this is moved to conftest


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import settings






SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.
                            DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL) # connect to database

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # some default 

Base = declarative_base() # models that we are going to define will be extended from this class






# Dependency   ->  it gets a connection/session to our database
# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()