from app import schemas
import pytest

def test_get_all_post(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    
    def validate(post):
        return schemas.PostOut(**post)
    post_map = map(validate, res.json())
    #post_lists = schemas.PostOut(**post_map)
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    #assert post_lists.Post.id == test_posts[0].id


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}") 
    assert res.status_code == 401


def test_get_one_post_does_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/8888") 
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content

@pytest.mark.parametrize("title, content, published", [ 
                         ("awsome new title", "awsome new content", True),
                         ("favourite pizza", "i love double cheeze", False),
                         ("tallest skyscrappers", "wahoo", True)])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", 
                                 json={"title": title, "content":content, "published":published})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_create_post_Default_publishes_true(authorized_client, test_posts, test_user):
    res = authorized_client.post("/posts/", 
                                 json={"title": "adanad", "content":"ndalndlakd"})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "adanad"
    assert created_post.content == "ndalndlakd"
    assert created_post.published == True
    assert created_post.owner_id == test_user["id"]

def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post("/posts/", 
                                 json={"title": "adanad", "content":"ndalndlakd"})
    assert res.status_code == 401

def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_authorized_user_delete_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_authorized_user_delete_post_does_not_exist(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/9999")
    assert res.status_code == 404

def test_authorized_user_delete_other_users_post(authorized_client, test_posts, test_user, test_user2): # remeber authorized_client is always logged in as test_user not test_user2 because we have setup our fixture like that
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_unauthorized_user_update_post(client, test_user, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}", json={"content":"jjskjadkaj"})
    assert res.status_code == 401

def test_authorized_user_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "jadjadja", 
        "content":"jjskjadkaj",
        "id": test_posts[0].id}
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data) 
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_user_update_other_users_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "jadjadja", 
        "content":"jjskjadkaj",
        "id": test_posts[3].id
        }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data) 
    assert res.status_code == 403

def test_authorized_user_update_post_does_not_exist(authorized_client, test_posts, test_user):
    data = {
        "title": "jadjadja", 
        "content":"jjskjadkaj",
        "id": test_posts[3].id
        }
    res = authorized_client.put(f"/posts/9999", json=data)
    assert res.status_code == 404