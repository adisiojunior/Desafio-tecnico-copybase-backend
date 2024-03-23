# Use a imagem base do Python
FROM python:3.9

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie os arquivos do projeto para o diretório de trabalho do contêiner
COPY . /app

# Instale as dependências do projeto
RUN pip install -r requirements.txt

# Exponha a porta 8000 para permitir o acesso ao servidor Django
EXPOSE 8000

# Inicie o servidor Django quando o contêiner for iniciado
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
