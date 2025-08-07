from collections import deque

_queue = deque()

def join_queue(user_id):
    if user_id not in _queue:
        _queue.append(user_id)
    return len(_queue)

def get_queue():
    return list(_queue)

def pop_players(n):
    players = []
    while _queue and len(players) < n:
        players.append(_queue.popleft())
    return players

def clear_queue():
    _queue.clear()
