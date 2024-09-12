import pytest
from todo_project import app, db, bcrypt
from todo_project.models import User, Task

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

@pytest.fixture
def init_database():
    db.create_all()
    user = User(username='testuser', password=bcrypt.generate_password_hash('password').decode('utf-8'))
    db.session.add(user)
    db.session.commit()
    yield db
    db.session.remove()
    db.drop_all()

def test_register(client):
    response = client.post('/register', data=dict(
        username='newuser',
        password='newpassword',
        confirm_password='newpassword'
    ), follow_redirects=True)
    assert b'Account Created For' in response.data

def test_login(client, init_database):
    response = client.post('/login', data=dict(
        username='testuser',
        password='password'
    ), follow_redirects=True)
    assert b'Login Successfull' in response.data

def test_add_task(client, init_database):
    client.post('/login', data=dict(
        username='testuser',
        password='password'
    ), follow_redirects=True)
    response = client.post('/add_task', data=dict(
        task_name='New Task'
    ), follow_redirects=True)
    assert b'Task Created' in response.data

def test_update_task(client, init_database):
    client.post('/login', data=dict(
        username='testuser',
        password='password'
    ), follow_redirects=True)
    client.post('/add_task', data=dict(
        task_name='Old Task'
    ), follow_redirects=True)
    task = Task.query.first()
    response = client.post(f'/all_tasks/{task.id}/update_task', data=dict(
        task_name='Updated Task'
    ), follow_redirects=True)
    assert b'Task Updated' in response.data

def test_delete_task(client, init_database):
    client.post('/login', data=dict(
        username='testuser',
        password='password'
    ), follow_redirects=True)
    client.post('/add_task', data=dict(
        task_name='Task to be deleted'
    ), follow_redirects=True)
    task = Task.query.first()
    response = client.get(f'/all_tasks/{task.id}/delete_task', follow_redirects=True)
    assert b'Task Deleted' in response.data
