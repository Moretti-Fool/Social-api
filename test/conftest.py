# here we'll define our fixtures and any fixture we define in this file will automatically be accessible to any of our tests within this package.
# so its package specific.


import pytest
from fastapi.testclient import TestClient
# from alembic import command
from testingDatabase.TDatabase import TestingSessionLocal, Base, engine
from app import models
from app.main import app
from app.database import get_db
from app.oauth2 import create_access_token







#ALEMBIC
# @pytest.fixture
# def Client():
#     command.upgrade("head")
#     yield TestClient(app)
#     command.downgrade("base")


#@pytest.fixture(scope="module") # by setting scope to module, the fixture is destroyed during teardown of the last test in the module. as default scope is set to functions means it will teardown after every function
# to avoid using scope = "module", as it makes our test dependent on each other, we will use default scope value which is set to function
@pytest.fixture()
def session(): # by doing this we can get access to database and pass queries
    models.Base.metadata.drop_all(bind=engine) 
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


#SQLALCHMEMY
#@pytest.fixture(scope="module")
@pytest.fixture()
def client(session):
    #return TestClient(app)
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    # run our code before we run our test
    # models.Base.metadata.drop_all(bind=engine) # we can also put this here, the advantages is putting here before yield is that, if we put this line after yield statement suppose we ran into failed test, we wll not run what happened in the database, but if we put this line first and use -x paramater which will stop testing if it run into failed test, we can see the state of the entry in the database 
    # models.Base.metadata.create_all(bind=engine) # first we will create tables then return testClient
    yield TestClient(app) # it adds flexibility in our code, as we dont have to create new test entries for every test
    #run our code after our test finishes
    #models.Base.metadata.drop_all(bind=engine) # after testing we will drop the tables



# this fixture will create a user, so that we can test our login route -> by doing this we can avoid setting scope parameter to module in fixture
@pytest.fixture
def test_user(client):
    user_data = {
        "email": "testuser@gmail.com",
        "password": "pass",
        "confirm_password": "pass"
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user



@pytest.fixture
def test_user2(client):
    user_data = {
        "email": "testuse2@gmail.com",
        "password": "pass",
        "confirm_password": "pass"
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user



@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, test_user2, session):
    post_data = [
        {"title": '1st title',
         "content": "1st content",
         "owner_id": test_user['id']},

         {"title": '2nd title',
         "content": "2nd content",
         "owner_id": test_user['id']},
         
         {"title": '3rd title',
         "content": "3rd content",
         "owner_id": test_user['id']},

         {"title": '4th title',
         "content": "4th content",
         "owner_id": test_user2['id']}
    ]

    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model, post_data)
    post = list(post_map)

    session.add_all(post)
    session.commit()

    get_posts = session.query(models.Post).all()
    return get_posts




