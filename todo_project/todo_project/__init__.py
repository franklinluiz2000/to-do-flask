from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.serving import WSGIRequestHandler
from flask_session import Session  # Para gerenciamento de sessões

app = Flask(__name__)

# Adcionando segurança
# Configurações de cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = True  # Habilita cookies apenas para HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Cookies não acessíveis via JavaScript
app.config['SESSION_COOKIE_PATH'] = '/'  # Define o escopo do cookie
app.config['SESSION_TYPE'] = 'filesystem'  # Opcional: Use sessões baseadas em sistema de arquivos

# Inicializa a sessão
Session(app)


# Adicionando segurança
@app.after_request
def add_security_headers(response):
    # Segurança de Frames
    response.headers['X-Frame-Options'] = 'DENY'
    # Impedir análise de MIME incorreta
    response.headers['X-Content-Type-Options'] = 'nosniff'
    # Política de Permissões
    response.headers['Permissions-Policy'] = 'geolocation=(self)'
    # Política de Segurança de Conteúdo
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self'; "
        "img-src 'self' data:; "
        "connect-src 'self'; "
        "font-src 'self'; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "form-action 'self'; "
        "frame-ancestors 'none';"  # Impede o embutimento em frames
    )

    # Controle de Cache
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    # Remover ou modificar o cabeçalho 'Server'
    response.headers.pop('Server', None)
    
    return response

app.wsgi_app = ProxyFix(app.wsgi_app)

# Isso ajuda a remover o 'Server' nas respostas HTTP
WSGIRequestHandler.server_version = ""
WSGIRequestHandler.sys_version = ""


app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login' 
login_manager.login_message_category = 'danger'

bcrypt = Bcrypt(app)

# Always put Routes at end
from todo_project import routes