import pytest
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from todo_project import create_app, db
from todo_project.models import User, Task

@pytest.fixture(scope='module')
def test_client():
    app = create_app('testing')
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
        yield testing_client
        with app.app_context():
            db.drop_all()

@pytest.fixture(scope='module')
def init_database():
    db.create_all()
    yield db
    db.drop_all()

def test_user_model(init_database):
    user = User(username='testuser', password=generate_password_hash('password'))
    db.session.add(user)
    db.session.commit()
    assert user.username == 'testuser'
    assert check_password_hash(user.password, 'password')

def test_register(test_client):
    response = test_client.post('/register', data=dict(
        username='newuser',
        password='newpassword',
        confirm_password='newpassword'
    ), follow_redirects=True)
    assert b'Account Created For' in response.data

def test_login(test_client, init_database):
    user = User(username='testuser', password=generate_password_hash('password'))
    db.session.add(user)
    db.session.commit()
    response = test_client.post('/login', data=dict(
        username='testuser',
        password='password'
    ), follow_redirects=True)
    assert b'Login Successful' in response.data

def test_add_task(test_client, init_database):
    user = User(username='testuser', password=generate_password_hash('password'))
    db.session.add(user)
    db.session.commit()
    test_client.post('/login', data=dict(
        username='testuser',
        password='password'
    ), follow_redirects=True)
    response = test_client.post('/add_task', data=dict(
        task_name='New Task'
    ), follow_redirects=True)
    assert b'Task Created' in response.data

def test_update_task(test_client, init_database):
    user = User(username='testuser', password=generate_password_hash('password'))
    db.session.add(user)
    db.session.commit()
    test_client.post('/login', data=dict(
        username='testuser',
        password='password'
    ), follow_redirects=True)
    test_client.post('/add_task', data=dict(
        task_name='Old Task'
    ), follow_redirects=True)
    task = Task.query.first()
    response = test_client.post(f'/all_tasks/{task.id}/update_task', data=dict(
        task_name='Updated Task'
    ), follow_redirects=True)
    assert b'Task Updated' in response.data

def test_delete_task(test_client, init_database):
    user = User(username='testuser', password=generate_password_hash('password'))
    db.session.add(user)
    db.session.commit()
    test_client.post('/login', data=dict(
        username='testuser',
        password='password'
    ), follow_redirects=True)
    test_client.post('/add_task', data=dict(
        task_name='Task to be deleted'
    ), follow_redirects=True)
    task = Task.query.first()
    response = test_client.get(f'/all_tasks/{task.id}/delete_task', follow_redirects=True)
    assert b'Task Deleted' in response.data

def test_account_page(test_client, init_database):
    user = User(username='testuser', password=generate_password_hash('password'))
    db.session.add(user)
    db.session.commit()
    test_client.post('/login', data=dict(
        username='testuser',
        password='password'
    ), follow_redirects=True)
    response = test_client.get('/account')
    assert response.status_code == 200
