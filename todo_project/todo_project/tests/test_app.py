import pytest
from todo_project import app, db, bcrypt
from todo_project.models import User, Task
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

# def test_register(client):
#     with client:
#         response = client.post(url_for('register'), data={
#             'username': 'testuser',
#             'password': 'password',
#             'confirm_password': 'password'
#         }, follow_redirects=True)
#         assert response.status_code == 200
#         assert b'Account Created For testuser' in response.data

# def test_login(client):
#     with client:
#         # First, register a user
#         client.post(url_for('register'), data={
#             'username': 'testuser',
#             'password': 'password',
#             'confirm_password': 'password'
#         }, follow_redirects=True)
        
#         # Then, log in with the same user
#         response = client.post(url_for('login'), data={
#             'username': 'testuser',
#             'password': 'password'
#         }, follow_redirects=True)
#         assert response.status_code == 200
#         assert b'Login Successfull' in response.data

# def test_add_task(client):
#     with client:
#         # First, register and log in a user
#         client.post(url_for('register'), data={
#             'username': 'testuser',
#             'password': 'password',
#             'confirm_password': 'password'
#         }, follow_redirects=True)
#         client.post(url_for('login'), data={
#             'username': 'testuser',
#             'password': 'password'
#         }, follow_redirects=True)
        
#         # Then, add a task
#         response = client.post(url_for('add_task'), data={
#             'task_name': 'Test Task'
#         }, follow_redirects=True)
#         assert response.status_code == 200
#         assert b'Task Created' in response.data
