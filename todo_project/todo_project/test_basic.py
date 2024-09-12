import pytest
from todo_project import app, db, bcrypt
from todo_project.models import User, Task
from flask_login import login_user
from werkzeug.security import generate_password_hash

# Testes Unitários

def test_password_hashing():
    password = 'my_password'
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    assert bcrypt.check_password_hash(hashed_password, password)

def test_user_model():
    user = User(username='testuser', password=generate_password_hash('password'))
    assert user.username == 'testuser'
    assert user.check_password('password') is True

# Testes de Integração

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

# Testes Funcionais

def test_about_page(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About' in response.data

def test_account_page(client, init_database):
    client.post('/login', data=dict(
        username='testuser',
        password='password'
    ), follow_redirects=True)
    response = client.get('/account')
    assert response.status_code == 200
    assert b'Account Settings' in response.data
