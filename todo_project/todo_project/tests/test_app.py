import pytest
from todo_project import create_app, db

@pytest.fixture
def app():
    app = create_app('testing')  # Ajuste para o nome da configuração de teste
    with app.app_context():
        db.create_all()  # Cria todas as tabelas do banco de dados para testes
        yield app
        db.drop_all()  # Remove todas as tabelas após os testes

@pytest.fixture
def client(app):
    return app.test_client()











# import pytest
# from todo_project import app, db, bcrypt
# from todo_project.models import User, Task

# Helper function to create a user
# def create_user(username, password):
#     hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
#     user = User(username=username, password=hashed_password)
#     db.session.add(user)
#     db.session.commit()
#     return user

# @pytest.fixture
# def client():
#     app.config['TESTING'] = True
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database
#     with app.test_client() as client:
#         with app.app_context():
#             db.create_all()
#         yield client
#         with app.app_context():
#             db.drop_all()


       
  

# def test_register(client):
#     # Simula um registro de usuário
#     response = client.post('/register', data={
#         'username': 'testuser',
#         'password': 'password',
#         'confirm_password': 'password'
#     }, follow_redirects=True)

#     assert response.status_code == 200
    
#     # Verifica se a mensagem de sucesso está presente no conteúdo retornado
#     assert b'Account Created For testuser' in response.data


# def test_login_logout(client):
#     # Cria um usuário para testar login
#     user = create_user('testuser', 'password')
    
#     # Testa login
#     response = client.post('/login', data={
#         'username': 'testuser',
#         'password': 'password'
#     }, follow_redirects=True)
    
#     assert response.status_code == 200
#     assert b'Login Successfull' in response.data
    
#     # Testa logout
#     response = client.get('/logout', follow_redirects=True)
#     assert b'Login' in response.data

# def test_add_task(client):
#     # Cria um usuário e faz login
#     user = create_user('testuser', 'password')
#     client.post('/login', data={'username': 'testuser', 'password': 'password'}, follow_redirects=True)
    
#     # Adiciona uma tarefa
#     response = client.post('/add_task', data={'task_name': 'Task 1'}, follow_redirects=True)
    
#     assert response.status_code == 200
#     assert b'Task Created' in response.data
    
#     # Verifica se a tarefa foi criada no banco de dados
#     task = Task.query.filter_by(content='Task 1').first()
#     assert task is not None
#     assert task.author == user

# def test_update_task(client):
#     # Cria um usuário, faz login e adiciona uma tarefa
#     user = create_user('testuser', 'password')
#     client.post('/login', data={'username': 'testuser', 'password': 'password'}, follow_redirects=True)
#     task = Task(content='Initial Task', author=user)
#     db.session.add(task)
#     db.session.commit()
    
#     # Atualiza a tarefa
#     response = client.post(f'/all_tasks/{task.id}/update_task', data={'task_name': 'Updated Task'}, follow_redirects=True)
    
#     assert response.status_code == 200
#     assert b'Task Updated' in response.data
    
#     # Verifica se a tarefa foi atualizada no banco de dados
#     updated_task = Task.query.get(task.id)
#     assert updated_task.content == 'Updated Task'
