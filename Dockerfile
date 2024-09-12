# Use a imagem oficial do Python como imagem base
FROM python:3.10

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

# Comando para iniciar a aplicação
CMD ["python", "todo_project/run.py"]
