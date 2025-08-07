from flask import current_app


class GameDAO:

    @staticmethod
    def create(players):
        db = current_app.get_db()
        # Ensure we have 4 players (pad with bots if needed)
        while len(players) < 4:
            players.append(f"bot_{len(players)}")

        print(players)

        nickname1 = players[0]
        nickname2 = players[1]
        nickname3 = players[2]
        nickname4 = players[3]
        result = 'in_progress'
        cursor = db.execute(
            "INSERT INTO games (white_player1, white_player2, black_player1, black_player2, result) VALUES (?, ?, ?, ?, ?)",
            (nickname1, nickname2, nickname3, nickname4, result))
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def get_partners(game_id):
        db = current_app.get_db()
        row = db.execute(
            'SELECT white_player1, white_player2, black_player1, black_player2 FROM games WHERE id = ?',
            (game_id, )).fetchone()
        if row is None:
            return []
        return [{
            'id': nickname,
            'nickname': nickname
        } for nickname in row if nickname]
