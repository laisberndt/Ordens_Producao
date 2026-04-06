# Sistema de Ordens de Produção

## 📌 Sobre o projeto
Este projeto é um sistema simples para gerenciamento de ordens de produção em uma indústria.

O sistema permite realizar as operações básicas de um CRUD:
- Criar ordens de produção (POST)
- Listar ordens cadastradas (GET)
- Atualizar o status das ordens (PUT)
- Excluir ordens do sistema (DELETE)

A aplicação conecta o front-end com o back-end por meio de uma API REST, permitindo a comunicação em tempo real com o banco de dados.

---

## 🧩 Estrutura do projeto

- `app.py` → Responsável pelo back-end (API Flask com rotas GET, POST, PUT e DELETE)  
- `database.py` → Gerencia a conexão e criação do banco de dados SQLite  
- `index.html` → Interface do usuário (formulário, tabela e integração com a API)  
- `ordens.db` → Banco de dados onde as informações são armazenadas  

---

## 📚 Tecnologias utilizadas

- Python  
- Flask  
- Flask-CORS  
- SQLite  
- HTML  
- CSS  
- JavaScript

---

## 🧰 Extensões utilizadas

- **GitLens** → Facilita a visualização do histórico de commits e alterações no código  
- **Python** → Suporte para desenvolvimento em Python no VS Code  
- **Python Debugger** → Permite executar e depurar o código passo a passo  
- **Pylance** → Oferece autocompletar, análise de código e sugestões inteligentes  
- **SQLite Viewer** → Gerencia bancos de dados SQLite dentro do VS Code  
- **REST Client** → Testa requisições HTTP direto no editor  
- **Docker** → Auxilia na criação e gerenciamento de containers para a aplicação  

---

## 📥 Clonar o repositório

No VS Code:

1. Abra o **Source Control**
2. Clique em **Clone Repository**
3. Cole o link do repositório
4. Escolha a pasta onde o projeto será salvo

---

## ⚙️ Configuração após o clone

No terminal (Ctrl + J), execute:

```bash
python -m venv venv
.\venv\Scripts\activate

pip install flask.cors
python.exe -m pip install --upgrade pip
pip install flask flask-cors
pip install -r requeriments.txt
