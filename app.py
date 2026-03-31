#BACK-END FLASK: ROTAS DA API REST

from flask import Flask, jsonify, request
from flask_cors import CORS
from database import init_bd, get_connection

#Criando uma instância da aplicação Flash
app = Flask(__name__, static_folder='static', static_url_path='')

#Habilitando os CORS
CORS(app)

#ROTA N1 - PÁGINA INICIAL
@app.route('/') #A "/" identifica que é um caminho
def index():
    #Alimenta o arquivo index.html da pasta static
    return app.send_static_file('index.html')

#ROTA N2 - STATUS API
@app.route('/status')
def status():
    '''Rota de verificação da API (Saúde)
    Retorna um JSON infornando que o servidor está ativo'''
    return jsonify({
        "status": "online",
        "sistema": "Sistema de Ordem de Producao",
        "versão": "1.0.0",
        "mensagem": "Ola Fabrica! API funcionando!"
    })

#ROTA N3 - LISTAR TODAS AS ORDENS (GET)
@app.route('/ordens', methods=['GET'])
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
    ordens = cursor.fetchall()
    conn.close()
    #Converte cada Row do SQLite em dicionário Python para serializar em JSON
    return jsonify([dict(o) for o in ordens])

#ROTA POR ID - BUSCAR UMA ORDEM ESPECÍFICA PELO ID
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
    
    #O '?' é substituído pelo valor de ordem_id de forma segura
    cursor.execute('SELECT * FROM ordens WHERE id = ?', (ordem_id,))
    ordem = cursor.fetchone() #Retorna um único registro ou None
    conn.close()
    
    if ordem is None:
        return jsonify({'erro': f'Ordem {ordem_id} nao encontrada!'}), 404 #Código de erro
    return jsonify(dict(ordem)), 200 #Código de sucesso

#ROTA - CRIAR NOVA ORDEM DE PRODUÇÃO (POST)
@app.route('ordens', methods=['POST'])
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
    dados = request.get_json()
    
    if not dados:
        return jsonify({'erro:': 'Body da requesicao ausente ou invalido.'}), 400
        #400 é para dados inválidos
    
    #Verificação de campo obrigatório (produto)
    produto = dados.get('produto', '').strip()
    if not produto:
        return jsonify({'erro': 'Campo "produto" e obrigatorio e nao pode ser vazio.'}), 400
    
    #Verificação de campo obrigatório (quantidade)
    quantidade = dados.get('quantidade')
    if quantidade is None:
        return jsonify({'erro': 'Campo "quantidade" e obrigatorio.'}), 400
    #Verifica se a quantidade é um número inteiro e positivo
    try:
        quantidade = int(quantidade)
        if quantidade <=0:
            raise ValueError()
    except (ValueError, TypeError):
        return jsonify({'erro': 'Campo "quantidade" deve ser um numero inteiro positivo.'}), 400
    
    #Status (*pendente, en amndamento, concluída) - opcional
    status_validos = ['Pendente','Em andamento','Concluida'] #Lista de valores
    status = dados.get('status', 'Pendente')
    if status not in status_validos:
        return jsonify({'erro': f'Status invalido. Use {status_validos}'}), 400
    
#PONTO DE PARTIDA
if __name__=='__main__':
    init_bd()
    app.run(debug=True, host='0.0.0.0', port=5000)