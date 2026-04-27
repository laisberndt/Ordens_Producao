# -----------------------------------------------------------------------------------
# app.py - SISTEMA DE ORDENS DE PRODUÇÃO - CRUD COMPLETO
# SENAI - JARAGUÁ DO SUL, SC - TÉCNICO EM CIBERSISTEMAS PARA AUTOMAÇÃO - 2026/1
# BACK-END FLASK: ROTAS DA API REST
# -----------------------------------------------------------------------------------

# Imports
from flask import Flask, jsonify, request # Micro-framework, projetado pra cirar aplicações web
from flask_cors import CORS
from database import init_bd, get_connection
import datetime

# Criando uma instância da aplicação Flash
app = Flask(__name__, static_folder='static', static_url_path='')

# Habilitando os CORS
CORS(app)

# ROTA N1 - PÁGINA INICIAL
@app.route('/') # A "/" identifica que é um caminho
def index():
    # Alimenta o arquivo index.html da pasta static
    return app.send_static_file('index.html')

# ROTA N2 - STATUS API
@app.route('/status')
def status():
    '''Rota de verificação da API (Saúde)
    Retorna um JSON infornando que o servidor está ativo'''

    conn = get_connection() # Estabelece comunicação com um banco de dados
    cursor = conn.cursor() # Funciona como um intermediário que permite enviar comandos SQL, gerenciar transações e buscar os resultados das consultas
    cursor.execute('SELECT COUNT(*) as total FROM ordens')
    resultado = cursor.fetchone() # Retorna um único registro ou None
    conn.close()

    return jsonify({
        "status": "online",
        "sistema": "Sistema de Ordens de Producao",
        "versao": "2.0.0",
        "total_ordens": resultado["total"],
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mensagem": "Ola Fabrica! API funcionando!"
    })

# ROTA N3 - LISTAR TODAS AS ORDENS (GET)
# Define uma rota da API no caminho /ordens/<ordem_id>
@app.route('/ordens', methods=['GET'])
# Função que será chamada quando a rota for acessada
def listar_ordens():
    '''
    Listar todas as ordens de produção cadastradas.
    Métodos HTTP: GET
    URL: http://localhost:5000/ordens
    Retorno: Lista de ordens em formato JSON
    '''
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ordens ORDER BY id DESC')
    ordens = cursor.fetchall() # Pega todos os resultados
    conn.close()

    # Converte cada Row do SQLite em dicionário Python para serializar em JSON
    return jsonify([dict(o) for o in ordens])

# ROTA POR ID - BUSCAR UMA ORDEM ESPECÍFICA PELO ID
@app.route('/ordens/<int:ordem_id>', methods=['GET'])
def buscar_ordem(ordem_id):
    '''
    Buscar uma única ordem de produção pelo ID.
    
    Parâmetros de URL:
        - ordem id(int) ID da ordem a ser buscada.
        
    Retorna: 
        200 + JSON da ordem, se for encontrada.
        404 + mensagem de erro, se não existir.
    '''
    conn = get_connection()
    cursor = conn.cursor()
    
    # O '?' é substituído pelo valor de ordem_id de forma segura
    cursor.execute('SELECT * FROM ordens WHERE id = ?', (ordem_id,))
    ordem = cursor.fetchone() 
    conn.close() #Fecha conexão
    
    if ordem is None:
        return jsonify({'erro': f'Ordem {ordem_id} nao encontrada!'}), 404 # Código de erro
    return jsonify(dict(ordem)), 200 # Código de sucesso

# ROTA N4 - CRIAR NOVA ORDEM DE PRODUÇÃO (POST)
@app.route('/ordens', methods=['POST'])
def criar_ordem():
    '''
    Cria uma nova ordem de produção a partir dos dados JSON enviados.
    
    Body esperado(JSON):
        produto     (str) : Nome do produto     - Obrigatório
        quantidade  (int) : Quantidade de peças - Obrigatório, >0
        status      (str) : Opcional            - Padrão: 'Pendente'
        
    Retorna: 
        201 : JSON da ordem criada, em caso de sucesso.
        404 : Mensagem de erro, se dados inválidos.
    '''
    dados = request.get_json() # quando vem JSON (API moderna)
    
    if not dados:
        return jsonify({'erro:': 'Body da requesicao ausente ou invalido.'}), 400 # Para dados inválidos
    
    # Verificação de campo obrigatório (produto)
    produto = dados.get('produto', '').strip() # Remove espaços no começo e no fim da string
    if not produto:
        return jsonify({'erro': 'Campo "produto" e obrigatorio e nao pode ser vazio.'}), 400
    
    # Verificação de campo obrigatório (quantidade)
    quantidade = dados.get('quantidade')
    if quantidade is None:
        return jsonify({'erro': 'Campo "quantidade" e obrigatorio.'}), 400
    # Verifica se a quantidade é um número inteiro e positivo
    try:
        quantidade = int(quantidade)
        if quantidade <=0:
            raise ValueError()
    except (ValueError, TypeError):
        return jsonify({'erro': 'Campo "quantidade" deve ser um numero inteiro positivo.'}), 400
    
    # Status (pendente, en amndamento, concluída) - opcional
    status_validos = ['Pendente','Em andamento','Concluida'] # Lista de valores
    status = dados.get('status', 'Pendente')
    
    if status not in status_validos:
        return jsonify({'erro': f'Status invalido. Use {status_validos}'}), 400
    
    # Inserção dos dados no banco
    conn = get_connection()
    cursor = conn.cursor()
    # Com o cursor.execute sempre vem o comando SQL
    cursor.execute('INSERT INTO ordens (produto, quantidade, status) VALUES (?, ?, ?)',
        (produto, quantidade, status))
    conn.commit()

    # Recuperando o ID que é gerado automaticamente pelo banco
    novo_id = cursor.lastrowid
    conn.close()

    # Buscar o registro que foi recém-criado
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ordens WHERE id = ?', (novo_id,))
    nova_ordem = cursor.fetchone() # Lê o máximo de resultados possíveis
    conn.close()

    return jsonify(dict(nova_ordem)), 201 # 201 retorna "created" com o registro completo

# ROTA N5 - ATUALIZAR O STATUS DE UMA ORDEM (PUT)
@app.route('/ordens/<int:ordem_id>', methods=['PUT'])
def atualizar_ordem(ordem_id):
    '''
    Atualiza o status de uma ordem de produção existente.
    Parâmetros de URL:
        ordem_id (int): ID da ordem a atualizar.
    Body esperado (JSON):
            status (str): Novo status. Valores aceitos: 'Pendente', 'Em andamento', 'Concluida'.
    Retorna:
        200 : JSON da ordem atualizada;
        400 : erro se status invalido;
        404 : erro se ordem nao encontrada.
    '''
    dados = request.get_json()

    if not dados:
        return jsonify({'erro': 'Body da requisicao ausente ou invalido'}), 400
    
    # Valida o campo status
    status_validos = ['Pendente', 'Em andamento', 'Concluida']
    novo_status = dados.get('status', '').strip()

    if not novo_status:
        return jsonify({'erro': 'o campo "status" e obrigatorio'}), 400
    
    if not novo_status in status_validos:
        return jsonify({'erro': f'Status invalido! Escolha entre {status_validos}'}), 400
        
    conn = get_connection()
    cursor = conn.cursor()
 
    # Verifica se a ordem consultada existe antes de atualizar
    cursor.execute('SELECT id FROM ordens WHERE id = ?', (ordem_id,))
    if cursor.fetchone() is None:
        conn.close()
        return jsonify({'erro': f'Ordem {ordem_id} nao encontrada.'}), 404
    
    # Atualiza o status
    cursor.execute('UPDATE ordens SET status = ? WHERE id = ?', (novo_status, ordem_id,))
    conn.commit()
    conn.close()

    # Retorna o registro atualizado
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ordens WHERE id = ?', (ordem_id,))
    ordem_atualizada = cursor.fetchone()
    conn.close()

    return jsonify(dict(ordem_atualizada)), 200

# ROTA N6 - REMOVER UMA ORDEM (DELETE)
@app.route('/ordens/<int:ordem_id>', methods=['DELETE'])
def remover_ordem(ordem_id):
    '''
    Remove permanentemente uma ordem de produção pelo ID.
    Parâmetros de URL:
        ordem_id (int): ID da ordem a ser removida.
    Retorna:
    200 + mensagem de confirmação.
    404 + erro se a ordem não for encontrada.
    '''
    conn = get_connection()
    cursor = conn.cursor()

    # Verifica se a ordem existe
    cursor.execute('SELECT id, produto FROM ordens WHERE id = ?', (ordem_id,))
    ordem = cursor.fetchone()

    if ordem is None:
        conn.close()
        return jsonify({'erro': f'Ordem {ordem_id} nao encontrada'}), 404
    
    # Guarda o nome do produto
    nome_produto = ordem['produto']
    
    # Executa a remoção permanente da ordem
    cursor.execute('DELETE FROM ordens WHERE id = ?', (ordem_id,))
    conn.commit()
    conn.close()

    return jsonify({'mensagem': f'Ordem {ordem_id} ({nome_produto}) removida com sucesso.', 'id_removido': ordem_id}), 200

# ROTA N7 - ATUALIZAR O PRODUTO E QUANTIDADE DE UMA ORDEM (PUT)
@app.route('/ordens/<int:ordem_id>/edit', methods=['PUT'])
def editar_ordem(ordem_id):
    '''
    Atualiza o nome e quantidade de uma ordem de produção existente.
    Parâmetros de URL:
        ordem_id (int): ID da ordem a atualizar.
    '''
    dados = request.get_json()

    if not dados:
        return jsonify({'erro': 'Body da requisicao ausente ou invalido'}), 400
    
    # Valida o campo produto
    novo_produto = dados.get('produto', '').strip()
    if not novo_produto:
        return jsonify({'erro': 'o campo "produto" e obrigatorio'}), 400

    # Valida o campo quantidade 
    nova_qtd = dados.get('quantidade')
    if nova_qtd is None:
        return jsonify({'erro': 'Campo "quantidade" e obrigatorio.'}), 400
    # Verifica se a quantidade é um número inteiro e positivo
    try:
        nova_qtd = int(nova_qtd)
        if nova_qtd <=0:
            raise ValueError()
    except (ValueError, TypeError):
        return jsonify({'erro': 'Campo "quantidade" deve ser um numero inteiro positivo.'}), 400
    
    conn = get_connection()
    cursor = conn.cursor()
 
    # Verifica se a ordem consultada existe antes de atualizar
    cursor.execute('SELECT id FROM ordens WHERE id = ?', (ordem_id,))
    if cursor.fetchone() is None:
        conn.close()
        return jsonify({'erro': f'Ordem {ordem_id} nao encontrada.'}), 404
    
    # Atualiza o produto e a quantidade
    cursor.execute('UPDATE ordens SET produto = ? WHERE id = ?', (novo_produto, ordem_id,))
    cursor.execute('UPDATE ordens SET quantidade = ? WHERE id = ?', (nova_qtd, ordem_id,))

    conn.commit()
    conn.close()

    # Retorna o registro atualizado
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ordens WHERE id = ?', (ordem_id,))
    ordem_atualizada = cursor.fetchone()
    conn.close()

    return jsonify(dict(ordem_atualizada)), 200

# PONTO DE PARTIDA
if __name__=='__main__':
    init_bd()
    app.run(debug=True, host='0.0.0.0', port=5000)