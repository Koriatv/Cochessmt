# app/controllers/train_controller.py

from flask import Blueprint, render_template, request
from app.dao.train_dao import get_puzzles

train_bp = Blueprint('train', __name__, url_prefix='/train')

@train_bp.route('/', methods=['GET'])
def train_home():
    # Recebe nível via query string: ?difficulty=medio
    difficulty = request.args.get('difficulty', 'facil')
    puzzles = get_puzzles(difficulty)
    return render_template('train.html',
                           puzzles=puzzles,
                           difficulty=difficulty)
