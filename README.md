# Sistema de Gerenciamento de Usuários

Este projeto consiste em uma aplicação CRUD para gerenciamento de usuários, desenvolvida com Vue.js para o frontend, Flask para o backend, e MongoDB como banco de dados.

## Estrutura do Projeto

- `backend/`: Contém a API Flask
- `frontend/`: Contém a aplicação Vue.js
- `parser.py`: Script para importar dados do arquivo JSON para o MongoDB
- `data.json`: Dados de exemplo para importação

## Pré-requisitos

- Python 3.8+
- Node.js 14+
- MongoDB

## Configuração

### 1. Configurar o MongoDB

- Instale o MongoDB
- Inicie o serviço MongoDB
- O banco de dados será criado automaticamente pelo script de importação

### 2. Configurar o Backend

```bash
cd backend
pip install -r requirements.txt
```

### 3. Configurar o Frontend

```bash
cd frontend
npm install
```

## Execução

### 1. Importar Dados

Execute o script de importação para carregar os dados iniciais:

```bash
python parser.py
```

### 2. Iniciar o Backend

```bash
cd backend
python app.py
```

O servidor Flask estará disponível em `http://localhost:5000`.

### 3. Iniciar o Frontend

```bash
cd frontend
npm run serve
```

A aplicação Vue.js estará disponível em `http://localhost:8080`.

## Funcionalidades

- Listagem de usuários em uma tabela com ordenação
- Visualização detalhada de um usuário
- Criação de novos usuários
- Edição de usuários existentes
- Exclusão de usuários (com confirmação) 