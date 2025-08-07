from flask import Blueprint, render_template, session, request, jsonify
from app.dao.matchmaking_dao import join_queue, get_queue, pop_players, clear_queue
from app.dao.game_dao import GameDAO  # assume já existe

match_bp = Blueprint('match', __name__)
REQUIRED = 1


@match_bp.route('/matchmaking')
def screen():
    return render_template('matchmaking.html', required=REQUIRED)


@match_bp.route('/matchmaking/join', methods=['POST'])
def join():
    user_id = session.get('user_email')
    count = join_queue(user_id)
    if count >= REQUIRED:
        players = pop_players(REQUIRED)
        if user_id not in players:
            players.insert(0, user_id)
        game_id = GameDAO.create(players)
        return jsonify(status='ready', game_id=game_id)
    return jsonify(status='waiting', count=count)


@match_bp.route('/matchmaking/status')
def status():
    q = get_queue()
    return jsonify(count=len(q), required=REQUIRED)


@match_bp.route('/matchmaking/complete', methods=['POST'])
def complete_with_bots():
    user_id = session.get('user_id')
    waiting = get_queue()
    pop_players(len(waiting))
    bots_needed = REQUIRED - len(waiting)
    players = waiting + ['bot'] * bots_needed
    clear_queue()
    if user_id not in players:
        players.insert(0, user_id)
    game_id = GameDAO.create(players)
    return jsonify(status='ready', game_id=game_id)
