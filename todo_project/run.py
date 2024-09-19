from dotenv import load_dotenv
from todo_project import app
import os

if __name__ == '__main__':
    host = os.getenv('FLASK_RUN_HOST', '127.0.0.1')
    app.run(host=host, port=5000, debug=True)


