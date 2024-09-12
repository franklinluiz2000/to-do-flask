import pytest
from todo_project import app, db, bcrypt
from todo_project.models import User, Task
from flask import url_for

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_about_page(client):
    with app.app_context():
        response = client.get(url_for('about'))
        assert response.status_code == 200
        assert b'About' in response.data

def test_register(client):
    with app.app_context():
        response = client.post(url_for('register'), data={
            'username': 'testuser',
            'password': 'password',
            'confirm_password': 'password'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Account Created For testuser' in response.data

def test_login(client):
    with app.app_context():
        # First, register a user
        client.post(url_for('register'), data={
            'username': 'testuser',
            'password': 'password',
            'confirm_password': 'password'
        }, follow_redirects=True)
        
        # Then, log in with the same user
        response = client.post(url_for('login'), data={
            'username': 'testuser',
            'password': 'password'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Login Successfull' in response.data

def test_add_task(client):
    with app.app_context():
        # First, register and log in a user
        client.post(url_for('register'), data={
            'username': 'testuser',
            'password': 'password',
            'confirm_password': 'password'
        }, follow_redirects=True)
        client.post(url_for('login'), data={
            'username': 'testuser',
            'password': 'password'
        }, follow_redirects=True)
        
        # Then, add a task
        response = client.post(url_for('add_task'), data={
            'task_name': 'Test Task'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Task Created' in response.data
