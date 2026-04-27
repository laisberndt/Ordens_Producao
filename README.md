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
- `ordens.db` → Banco de dados onde as informações são armazenadas  
- 📁 `static` → Arquivos do front-end  
  - `index.html` → Interface do usuário (formulário e tabela)  
  - `script.js` → Lógica da aplicação e comunicação com a API (fetch)  
  - `style.css` → Estilização da interface  

---

## ⚙️ Funcionamento do sistema

### 🔙 Back-end
Desenvolvido em **Python com Flask**, responsável por:
- Criar rotas da API (GET, POST, PUT, DELETE)
- Processar requisições
- Interagir com o banco de dados SQLite

### 🔜 Front-end
Desenvolvido com **HTML, CSS e JavaScript**
Responsável por:
- Interface do usuário
- Captura de dados
- Comunicação com a API usando `fetch()`

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

## 🧰 Ferramentas e extensões recomendadas

- **GitLens** → Histórico de commits e rastreamento de alterações  
- **Python (VS Code)** → Suporte à linguagem Python  
- **Python Debugger** → Depuração do código  
- **Pylance** → Autocompletar e análise inteligente  
- **SQLite Viewer** → Visualização do banco de dados  
- **REST Client** → Teste de requisições HTTP  

---

## 📥 Como clonar o projeto

No **VS Code**:

1. Acesse o menu **Source Control**
2. Clique em **Clone Repository**
3. Cole o link do repositório
4. Escolha a pasta de destino

Ou via terminal:

```bash
git clone <URL_DO_REPOSITORIO>
```
---

## ⚙️ Configuração após o clone

No terminal (Ctrl + J), execute:

```bash
python -m venv venv
.\venv\Scripts\activate

pip install -r requeriments.txt

python app.py
```
Depois, acesse no navegador:
```bash
http://localhost:5000
