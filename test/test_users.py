from fastapi.testclient import TestClient
from app.main import app
from app import schemas

client = TestClient(app)



def test_create_user():
    res = client.post("/users/", json={
        "email":"user_t3@gmail.com",
        "password":"pass",
        "confirm_password":"pass"
    })
    new_user = schemas.UserOut(**res.json()) # it will verify the values that we passing through pydantic model
    assert new_user.email == "user_t3@gmail.com"
    assert res.status_code == 201
    