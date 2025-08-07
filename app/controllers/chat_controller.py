# app/controllers/chat_controller.py

from flask import Blueprint, request, session, jsonify
from datetime import datetime
from app.dao.chat_dao import save_message, get_messages

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat/send', methods=['POST'])
def send_chat():
    data = request.get_json()
    game_id = data.get('game_id')
    text    = data.get('text', '').strip()
    user    = session.get('user_email', 'Anônimo')
    ts      = datetime.utcnow().isoformat()

    if not game_id or not text:
        return jsonify(status='error', msg='Parâmetros faltando'), 400

    save_message(game_id, user, text, ts)
    
    msgs = get_messages(game_id) #recarrega as mensagens depois de salvar
    return jsonify(status='ok', messages=msgs) #retorna as mensagens atualizadas

@chat_bp.route('/chat/fetch')
def fetch_chat():
    game_id = request.args.get('game_id')
    if not game_id:
        return jsonify(status='error', msg='game_id faltando'), 400

    msgs = get_messages(game_id)
    return jsonify(status='ok', messages=msgs)