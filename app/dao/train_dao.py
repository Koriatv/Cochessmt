# app/dao/train_dao.py

# Exemplo de banco de puzzles em memória; troque por consultas reais se tiver tabela no DB
_PUZZLES = {
    'facil': [
        {'id': 1, 'fen': '8/8/8/8/4K3/8/4k3/8 w - - 0 1', 'hint': 'Mova o rei'},
        {'id': 2, 'fen': '8/3P4/8/8/8/8/3k4/3K4 w - - 0 1', 'hint': 'Promova o peão'}
    ],
    'medio': [
        {'id': 3, 'fen': 'rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2', 'hint': 'Controle o centro'},
        {'id': 4, 'fen': '8/8/4k3/4P3/4K3/8/8/8 w - - 0 1', 'hint': 'Tática de zugzwang'}
    ],
    'dificil': [
        {'id': 5, 'fen': '8/8/8/3k4/8/4PN2/3K4/8 w - - 0 1', 'hint': 'Material a mais'},
        {'id': 6, 'fen': 'r3k2r/pppb1ppp/2np1n2/4p3/2B1P3/2N2N2/PPPB1PPP/R3K2R w KQkq - 0 1', 'hint': 'Abertura complexa'}
    ]
}

def get_puzzles(difficulty: str):
    # Map English difficulty names to Portuguese keys
    difficulty_map = {
        'easy': 'facil',
        'medium': 'medio', 
        'hard': 'dificil'
    }
    
    # Get the mapped difficulty or default to 'facil'
    mapped_difficulty = difficulty_map.get(difficulty, 'facil')
    return _PUZZLES.get(mapped_difficulty, _PUZZLES['facil'])
