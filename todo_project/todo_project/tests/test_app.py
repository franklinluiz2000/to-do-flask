import pytest
from todo_project import app, db
from flask import url_for

@pytest.fixture
def app_context():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app_context):
    return app_context.test_client()

def test_about_page(client):
    with client:
        response = client.get(url_for('/about'))
        assert response.status_code == 200
        assert b'About' in response.data

