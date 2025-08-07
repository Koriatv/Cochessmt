# app/dao/chat_dao.py

from collections import defaultdict

# Dicionário game_id → lista de mensagens
_messages = defaultdict(list)

def save_message(game_id: str, username: str, text: str, timestamp: str):
    _messages[game_id].append({
        'user': username,
        'text': text,
        'timestamp': timestamp
    })

def get_messages(game_id: str):
    return _messages.get(game_id, [])
