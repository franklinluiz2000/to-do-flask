from dotenv import load_dotenv
from todo_project import app
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

if __name__ == '__main__':
    # Defina o host e a porta para o Heroku e para rodar localmente
    host = os.getenv('FLASK_RUN_HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))  # Use a porta do Heroku se disponível
    app.run(host=host, port=port)
