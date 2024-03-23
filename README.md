# Instruções para Executar o Projeto Django Rest Framework

## Clonando o Repositório

1. Clone o repositório do projeto para o seu ambiente local:
    ```bash
    git clonehttps://github.com/adisiojunior/Desafio-tecnico-copybase-backend.git
    ```

## Instalação das Dependências

2. Navegue até o diretório do projeto clonado:
    ```bash
    cd subscription_analytics_project
    ```

3. Instale as dependências necessárias do projeto utilizando o pip:
    ```bash
    pip install -r requirements.txt
    ```

## Configuração do Banco de Dados

4. Execute as migrações do banco de dados para aplicar as alterações do modelo:
    ```bash
    python manage.py migrate
    ```

## Execução do Servidor de Desenvolvimento

5. Inicie o servidor de desenvolvimento Django:
    ```bash
    python manage.py runserver
    ```

## Acesso ao Endpoint de Upload

6. Abra um navegador da web e acesse o seguinte URL para acessar o endpoint de upload:
    ```
    http://localhost:8000/api/upload/
    ```

Isso deve exibir o endpoint para upload de arquivos, conforme configurado no seu projeto Django Rest Framework.

Certifique-se de ajustar o URL e o comando de clonagem do repositório de acordo com o seu caso específico.
