# API Backend — Projeto Integrado de Software

API RESTful construída em Python com **FastAPI** e **SQLAlchemy**, utilizando **PostgreSQL** como banco de dados relacional para persistência.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python 3.x | Linguagem principal |
| FastAPI | Construção e gerenciamento das rotas RESTful |
| SQLAlchemy | Mapeamento Objeto-Relacional e gerenciamento de sessões |
| PostgreSQL | Banco de dados relacional para persistência |
| Pydantic | Validação de tipos e schemas de dados |
| python-dotenv | Isolamento de credenciais em arquivos de ambiente |

---

## 🚀 Como Rodar o Projeto Localmente

### 1. Configurar o Ambiente Virtual

Crie e ative o ambiente virtual na pasta raiz do projeto:

```bash
# Criar o ambiente virtual
python -m venv .venv

# Ativar no Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Ativar no Linux/Mac
source .venv/bin/activate
```

### 2. Instalar as Dependências

```bash
pip install -r requirements.txt
```

### 3. Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com base no `.env.example` fornecido:

```env
DB_USER=seu_usuario_postgres
DB_PASSWORD=sua_senha_do_banco
DB_NAME=nome_do_seu_banco
DB_HOST=localhost
DB_PORT=5432
```

### 4. Executar o Servidor

```bash
uvicorn main:app --reload
```

---

## 📌 Rotas da API

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/` | Rota raiz de teste |
| `GET` | `/mensagens` | Recupera mensagens com suporte a paginação (`skip`, `limit`) |
| `POST` | `/mensagens` | Registra uma nova mensagem com validação de corpo JSON |