from django import db
from todo_project.todo_project.models import Task, User


def test_user_repr():
    user = User(username='testuser', password='password')
    assert repr(user) == "User('testuser')"

def test_task_repr():
    task = Task(content='Test Task', user_id=1)
    assert repr(task) == f"Task('Test Task', '{task.date_posted}', '1')"

def test_create_user_and_task(client):
    # Criar um usuário
    user = User(username='testuser', password='password')
    db.session.add(user)
    db.session.commit()
    
    # Verificar se o usuário foi criado
    assert User.query.filter_by(username='testuser').first() is not None

    # Criar uma tarefa para o usuário
    task = Task(content='Test Task', user_id=user.id)
    db.session.add(task)
    db.session.commit()
    
    # Verificar se a tarefa foi criada
    assert Task.query.filter_by(content='Test Task').first() is not None

def test_user_tasks_relationship():
    user = User(username='testuser', password='password')
    task1 = Task(content='Test Task 1', user_id=user.id)
    task2 = Task(content='Test Task 2', user_id=user.id)
    db.session.add(user)
    db.session.add(task1)
    db.session.add(task2)
    db.session.commit()
    
    assert len(user.tasks) == 2
    assert task1 in user.tasks
    assert task2 in user.tasks

def test_register(client):
    response = client.post('/register', data=dict(
        username='newuser',
        password='newpassword',
        confirm_password='newpassword'
    ), follow_redirects=True)
    assert b'Account Created For newuser' in response.data

def test_login(client):
    User(username='testuser', password=generate_password_hash('password')).save()  # type: ignore # Crie um usuário para teste
    response = client.post('/login', data=dict(
        username='testuser',
        password='password'
    ), follow_redirects=True)
    assert b'Login Successfull' in response.data
