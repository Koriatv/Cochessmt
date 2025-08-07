document.addEventListener("DOMContentLoaded", () => {
    // ---------------- Chessboard Initialization ----------------
    const board = document.getElementById('chessboard');
    const gameId = document.body.dataset.gameId;

    // Oculta mensagens flash se existirem
    const flash = document.querySelector('.flash-messages');
    if (flash) {
        setTimeout(() => {
            flash.style.display = 'none';
        }, 4000);
    }

    if (board) {
        createBoard(board, gameId);
    }

    // ---------------- Matchmaking Initialization ----------------
    const statusEl = document.getElementById('status');
    const btnBots  = document.getElementById('btn-bots');

    if (statusEl && btnBots) {
        joinMatchmaking();
        setInterval(pollMatchmakingStatus, 2000);
        btnBots.addEventListener('click', completeWithBots);
    }

    // ---------------- Chat Initialization ----------------
    const chatBox    = document.getElementById('chat-box');
    const sendButton = document.getElementById('chat-send-button');
    const chatInput  = document.getElementById('chat-input');

    if (chatBox && sendButton && chatInput && gameId) {
        // Carregar mensagens iniciais
        pollChatMessages();
        
        // Polling de mensagens a cada 1s
        setInterval(pollChatMessages, 1000);

        // Enviar no clique
        sendButton.addEventListener('click', sendChatMessage);

        // Enviar no Enter
        chatInput.addEventListener('keypress', e => {
            if (e.key === 'Enter') {
                sendChatMessage();
                e.preventDefault();
            }
        });
    }
});

const pieces = {
    'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
    'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙'
};

const initialBoard = [
    'r','n','b','q','k','b','n','r',
    'p','p','p','p','p','p','p','p',
    '','','','','','','','',
    '','','','','','','','',
    '','','','','','','','',
    '','','','','','','','',
    'P','P','P','P','P','P','P','P',
    'R','N','B','Q','K','B','N','R'
];

let selectedSquare = null;

/**
 * Cria o tabuleiro e posiciona as peças iniciais
 */
function createBoard(board, gameId) {
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const square = document.createElement('div');
            square.classList.add('square');
            square.classList.add((row + col) % 2 === 0 ? 'white' : 'black');
            square.dataset.row = row;
            square.dataset.col = col;

            const piece = initialBoard[row * 8 + col];
            if (piece) square.textContent = pieces[piece];

            square.addEventListener('click', () => handleClick(square, board, gameId));
            board.appendChild(square);
        }
    }
}

/**
 * Trata clique numa casa: seleciona ou movimenta
 */
function handleClick(square, board, gameId) {
    if (selectedSquare) {
        selectedSquare.classList.remove('selected');

        const fromRow = parseInt(selectedSquare.dataset.row);
        const fromCol = parseInt(selectedSquare.dataset.col);
        const toRow   = parseInt(square.dataset.row);
        const toCol   = parseInt(square.dataset.col);
        const piece   = selectedSquare.textContent;

        square.textContent       = piece;
        selectedSquare.textContent = '';
        selectedSquare = null;

        if (gameId) {
            fetch("/move", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    game_id: gameId,
                    from: [fromRow, fromCol],
                    to:   [toRow, toCol],
                    piece: piece.toLowerCase()
                })
            }).catch(console.error);
        }

    } else if (square.textContent !== '') {
        selectedSquare = square;
        square.classList.add('selected');
    }
}

/*****************************************************************************
 *                      FUNÇÕES DE MATCHMAKING                                *
 *****************************************************************************/

/**
 * Entra na fila de matchmaking
 */
function joinMatchmaking() {
    fetch('/matchmaking/join', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'ready') {
                window.location = `/game?game_id=${data.game_id}`;
            }
        })
        .catch(console.error);
}

/**
 * Consulta número de jogadores aguardando e atualiza a UI
 */
function pollMatchmakingStatus() {
    fetch('/matchmaking/status')
        .then(res => res.json())
        .then(data => {
            const statusEl = document.getElementById('status');
            const btnBots  = document.getElementById('btn-bots');
            if (!statusEl || !btnBots) return;

            statusEl.textContent = `${data.count}/${data.required}`;

            if (data.count >= data.required) {
                btnBots.style.display = 'none';
                return;
            }

            if (data.count > 1) {
                btnBots.style.display = 'block';
            }
        })
        .catch(console.error);
}

/**
 * Completa a partida com bots e inicia o jogo
 */
function completeWithBots() {
    fetch('/matchmaking/complete', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            window.location = `/game?game_id=${data.game_id}`;
        })
        .catch(console.error);
}

/*****************************************************************************
 *                          FUNÇÕES DE CHAT                                  *
 *****************************************************************************/

/**
 * Envia uma mensagem de chat para o servidor
 */
function sendChatMessage() {
    const input  = document.getElementById('chat-input');
    const gameId = document.body.dataset.gameId;
    const text   = input.value.trim();
    if (!text) return;

    fetch('/chat/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ game_id: gameId, text: text })
    })
    .then(res => res.json())
    .then(json => {
        if (json.status === 'ok') {
            input.value = '';
            // Atualizar imediatamente as mensagens
            if (json.messages) {
                updateChatBox(json.messages);
            }
        }
    })
    .catch(console.error);
}

/**
 * Busca mensagens novas do chat e atualiza a caixa
 */
function pollChatMessages() {
    const gameId = document.body.dataset.gameId;
    if (!gameId) return;

    fetch(`/chat/fetch?game_id=${gameId}`)
        .then(res => res.json())
        .then(json => {
            if (json.status === 'ok') {
                updateChatBox(json.messages);
            }
        })
        .catch(console.error);
}

/**
 * Atualiza a caixa de chat com as mensagens
 */
function updateChatBox(messages) {
    const box = document.getElementById('chat-box');
    if (!box) return;
    
    box.innerHTML = '';
    messages.forEach(msg => {
        const div = document.createElement('div');
        div.innerHTML = `<strong>${msg.user}</strong>: ${msg.text}`;
        box.appendChild(div);
    });
    box.scrollTop = box.scrollHeight;
}
