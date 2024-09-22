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

# Exponha a porta que a aplicação irá rodar
EXPOSE 5000

# Comando para iniciar a aplicação usando gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "todo_project.todo_project.run:app"]

