import pytest
from app import schemas, models

@pytest.fixture
def votes(test_posts, session, test_user):
    new_vote = models.Votes(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()


def test_votes_on_posts(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json= {"post_id": test_posts[0].id, "dir":1})
    assert res.status_code == 201

def test_unauthorized_vote_on_post(client, test_posts):
    res = client.post("/vote/", json = {"post_id": test_posts[3].id, "dir":1})
    assert res.status_code == 401

def test_votes_twice_posts(authorized_client, test_posts, votes):
    res = authorized_client.post("/vote/", json= {"post_id": test_posts[3].id, "dir":1})
    assert res.status_code == 409


def test_delete_vote(authorized_client, test_posts, votes):
    res = authorized_client.post("/vote/", json = {"post_id": test_posts[3].id, "dir":0})
    assert res.status_code == 201

def test_delete_vote_non_exist_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json = {"post_id": test_posts[3].id, "dir":0})
    assert res.status_code == 404

def test_unauthorized_delete_vote_non_exist_post(client, test_posts, votes):
    res = client.post("/vote/", json = {"post_id": test_posts[3].id, "dir":0})
    assert res.status_code == 401

def test_vote_non_exist(authorized_client):
    res = authorized_client.post("/vote/", json = {"post_id": 4394294, "dir":1})
    assert res.status_code == 404