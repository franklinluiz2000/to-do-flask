import os
from todo_project import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use a porta do Heroku ou 5000 localmente
    app.run(host='127.0.0.1', port=port, debug=True)
