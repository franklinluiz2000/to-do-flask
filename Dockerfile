# Use a imagem oficial do Python como imagem base
FROM python:3.10-slim

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie os arquivos de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências
RUN pip3 install --no-cache-dir -r requirements.txt

# Copie todo o código do projeto para o diretório de trabalho
COPY . .

# Exponha a porta que a aplicação irá rodar (Heroku usará uma porta diferente)
EXPOSE 5000

# Defina a variável de ambiente para a aplicação Flask
ENV FLASK_APP=todo_project/run.py

# Comando para iniciar a aplicação usando gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "todo_project.run:app"]
