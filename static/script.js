// URL base da API
const API_URL = 'http://localhost:5000';

/* ————————————————————————————————————————————————————————————————
   1. VERIFICAÇÃO DE STATUS
   ———————————————————————————————————————————————————————————————— */
async function verificarStatus() {
    const badge = document.getElementById('status-badge');
    try {
        const resp = await fetch(`${API_URL}/status`);
        const dados = await resp.json();
        badge.textContent = `API Online | ${dados.total_ordens} ordens`;
        badge.className = 'online';
    } catch (erro) {
        badge.textContent = 'API Offline';
        badge.className = 'offline';
    }
}

/* ————————————————————————————————————————————————————————————————
   2. CARREGAR ORDENS (GET)
   ———————————————————————————————————————————————————————————————— */
async function carregarOrdens() {
    const loading = document.getElementById('loading');
    const semDados = document.getElementById('sem-dados');
    const tabela = document.getElementById('tabela-ordens');
    const corpo = document.getElementById('corpo-tabela');

    loading.classList.remove('oculto');
    tabela.classList.add('oculto');
    semDados.classList.add('oculto');

    try {
        const resposta = await fetch(`${API_URL}/ordens`);
        const ordens = await resposta.json();

        loading.classList.add('oculto');

        if (ordens.length === 0) {
            semDados.classList.remove('oculto');
            return;
        }

        corpo.innerHTML = ordens.map(ordem => `
            <tr id="linha-${ordem.id}">
                <td>${ordem.id}</td>
                <td class="col-produto">${ordem.produto}</td>
                <td class="col-quantidade">${ordem.quantidade}</td>
                <td>${renderizarBadge(ordem.status)}</td>
                <td>${ordem.criado_em}</td>
                <td>
                    <select class="select-status" onchange="atualizarStatus(${ordem.id}, this.value)">
                        <option value="Pendente" ${ordem.status === 'Pendente' ? 'selected' : ''}>Pendente</option>
                        <option value="Em andamento" ${ordem.status === 'Em andamento' ? 'selected' : ''}>Em andamento</option>
                        <option value="Concluida" ${ordem.status === 'Concluida' ? 'selected' : ''}>Concluída</option>
                    </select>
                    
                    <button class="btn-excluir" onclick="excluirOrdem(${ordem.id})">Excluir</button>

                    <button class="btn-editar" onclick="editarOrdem(${ordem.id})">Editar</button>
                </td>
            </tr>
        `).join('');

        tabela.classList.remove('oculto');

    } catch (erro) {
        loading.classList.add('oculto');
        console.error(erro);
        exibirMensagem('Erro ao carregar dados.', 'erro');
    }
}

/* ————————————————————————————————————————————————————————————————
   3. CRIAR ORDENS (POST)
   ———————————————————————————————————————————————————————————————— */
async function criarOrdem() {
    // Captura os valores dos campos HTML
    const produto = document.getElementById('produto').value.trim();
    const quantidade = document.getElementById('quantidade').value;
    const status = document.getElementById('status-novo').value;

    // Validacao no front-end (antes de chamar a API)
    if (!produto) {
        exibirMensagem('Preencha o nome do produto.', 'erro');
        document.getElementById('produto').focus();
        return;
    }

    if (!quantidade || Number(quantidade) <= 0) {
        exibirMensagem('Informe uma quantidade valida (numero positivo).', 'erro');
        document.getElementById('quantidade').focus();
        return;
    }

    // Desabilita o botao para evitar duplo clique
    const btn = document.getElementById('btn-cadastrar');
    btn.disabled = true;
    btn.textContent = 'Cadastrando...';

    try {
        const resposta = await fetch(`${API_URL}/ordens`, {
            method: 'POST',
            // Content-Type diz ao Flask que o body e JSON
            headers: { 'Content-Type': 'application/json' },
            // JSON.stringify converte objeto JS em string JSON
            body: JSON.stringify({
                produto: produto,
                quantidade: Number(quantidade),
                status: status
            })
        });

        const dados = await resposta.json();

        if (resposta.ok) { // resposta.ok = true para status 200-299
            exibirMensagem(`Ordem #${dados.id} cadastrada com sucesso!`, 'sucesso');
            limparFormulario();
            await carregarOrdens();   // Atualiza a tabela
            await verificarStatus();  // Atualiza o contador no cabecalho
        } else {
            // Exibe a mensagem de erro retornada pelo Flask
            exibirMensagem(dados.erro || 'Erro ao cadastrar.', 'erro');
        }

    } catch (erro) {
        exibirMensagem('Erro de conexao com a API.', 'erro');
        console.error(erro);
    } finally {
        // O bloco finally executa SEMPRE, com ou sem erro
        btn.disabled = false;
        btn.textContent = 'Cadastrar Ordem';
    }
}

// Limpa os campos do formulario apos cadastro bem-sucedido
function limparFormulario() {
    document.getElementById('produto').value = '';
    document.getElementById('quantidade').value = '';
    document.getElementById('status-novo').value = 'Pendente';
}

/* ————————————————————————————————————————————————————————————————
   4. EDITAR PRODUTO/QUANTIDADE (PUT)
   ———————————————————————————————————————————————————————————————— */
async function editarOrdem(id) {
    const linha = document.getElementById(`linha-${id}`);
    const produtoAtual = linha.querySelector('.col-produto').textContent;
    const qtdAtual = linha.querySelector('.col-quantidade').textContent;

    const novoProduto = window.prompt("Editar nome do produto:", produtoAtual);
    if (novoProduto === null || novoProduto.trim() === "") return;

    const novaQuantidade = window.prompt("Editar quantidade:", qtdAtual);
    if (novaQuantidade === null || isNaN(novaQuantidade) || novaQuantidade <= 0) {
        exibirMensagem("Quantidade inválida.", "erro");
        return;
    }


    try {
        const resposta = await fetch(`${API_URL}/ordens/${id}/edit`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                produto: novoProduto,
                quantidade: Number(novaQuantidade),
            })
        });

        if (resposta.ok) {
            exibirMensagem('Ordem atualizada com sucesso!', 'sucesso');
            // Atualiza a linha visualmente
            linha.querySelector('.col-produto').textContent = novoProduto;
            linha.querySelector('.col-quantidade').textContent = novaQuantidade;
        } else {
            const dados = await resposta.json();
            exibirMensagem(dados.erro || 'Erro ao editar.', 'erro');
        }
    } catch (erro) {
        exibirMensagem('Erro de conexão.', 'erro');
    }
}

/* ————————————————————————————————————————————————————————————————
   5. ATUALIZAR STATUS (PUT)
   ———————————————————————————————————————————————————————————————— */
   async function atualizarStatus(id, novoStatus) {
    try {
        // Envia uma requisição PUT para a rota específica da ordem
        const resposta = await fetch(`${API_URL}/ordens/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: novoStatus })
        });

        const dados = await resposta.json();

        if (resposta.ok) {
            exibirMensagem(`Status da Ordem #${id} atualizado para '${novoStatus}'.`, 'sucesso');
            
            // Atualiza apenas o badge na linha, sem recarregar a tabela inteira (mais rápido)
            const linha = document.getElementById(`linha-${id}`);
            if (linha) {
                const tdStatus = linha.cells[4]; // Localiza a célula do status (coluna 4)
                tdStatus.innerHTML = renderizarBadge(novoStatus); // Troca o HTML pelo novo badge
            }
            await verificarStatus(); // Atualiza o contador geral no topo
        } else {
            exibirMensagem(dados.erro || 'Erro ao atualizar status.', 'erro');
            // Se der erro, recarrega a tabela para voltar o select ao valor original
            await carregarOrdens();
        }
    } catch (erro) {
        exibirMensagem('Erro de conexao.', 'erro');
        console.error(erro);
    }
}

/* ————————————————————————————————————————————————————————————————
   6. EXCLUIR ORDEM (DELETE)
   ———————————————————————————————————————————————————————————————— */
async function excluirOrdem(id) {
    if (!window.confirm(`Deseja realmente excluir a Ordem #${id}?`)) return;

    try {
        const resposta = await fetch(`${API_URL}/ordens/${id}`, { method: 'DELETE' });
        if (resposta.ok) {
            exibirMensagem('Ordem removida.', 'sucesso');
            document.getElementById(`linha-${id}`).remove();
            
            const corpo = document.getElementById('corpo-tabela');
            if (corpo.children.length === 0) {
                document.getElementById('tabela-ordens').classList.add('oculto');
                document.getElementById('sem-dados').classList.remove('oculto');
            }
            await verificarStatus();
        }
    } catch (erro) {
        exibirMensagem('Erro ao excluir.', 'erro');
    }
}

/* ————————————————————————————————————————————————————————————————
   7. UTILITÁRIOS
   ———————————————————————————————————————————————————————————————— */
function renderizarBadge(status) {
    const classes = {
        'Pendente': 'badge badge-pendente',
        'Em andamento': 'badge badge-andamento',
        'Concluida': 'badge badge-concluida',
    };
    return `<span class="${classes[status] || 'badge'}">${status}</span>`;
}

function exibirMensagem(texto, tipo) {
    const div = document.getElementById('mensagem');
    div.textContent = texto;
    div.className = `mensagem ${tipo}`;
    div.classList.remove('oculto');
    setTimeout(() => div.classList.add('oculto'), 4000);
}

window.onload = async () => {
    await verificarStatus();
    await carregarOrdens();
};