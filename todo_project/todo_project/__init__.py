from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

login_manager.login_view = 'login'
login_manager.login_message_category = 'danger'

def create_app(config_class=None):
    app = Flask(__name__)

    # Configuração da aplicação
    app.config['SECRET_KEY'] = '45cf93c4d41348cd9980674ade9a7356'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    # Inicializar as extensões
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Registrar rotas
    from todo_project import routes
    app.register_blueprint(routes.bp)  # Certifique-se de que as rotas estão em um blueprint

    return app
