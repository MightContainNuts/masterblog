from app import open_json


def test_default():
    posts = open_json()
    assert not posts
