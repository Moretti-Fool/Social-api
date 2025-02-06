import pytest
from jose import jwt
from app import schemas
from app.config import settings



#app.dependency_overrides[get_db] = override_get_db
#client = TestClient(app)



#user registration test
def test_create_user(client):
    res = client.post("/users/", json={
        "email":"testuser@gmail.com",
        "password":"pass",
        "confirm_password":"pass"
    })
    new_user = schemas.UserOut(**res.json()) # it will verify the values that we passing through pydantic model
    assert new_user.email == "testuser@gmail.com"
    assert res.status_code == 201


#user login test
def test_login_user(client, test_user):
    res = client.post("/login", data={
        "username":test_user['email'],
        "password":test_user['password']
    })
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type ==  "bearer"
    assert res.status_code == 200
    

# incorrect login credentials test
@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'pass', 403),
    ('testuser@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    ( None,'pass', 422),
    ('testuser@gmail.com', None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={
        "username": email,
        "password": password
    })
    print(res.json())
    assert res.status_code == status_code
    #assert res.json().get('detail') == 'Invalid Credentials'