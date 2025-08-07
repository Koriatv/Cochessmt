from app.controllers import auth_controller, user_controller


def configure_routes(app):
    app.add_url_rule('/', view_func=auth_controller.home)
    app.add_url_rule('/login',
                     view_func=auth_controller.login,
                     methods=['GET', 'POST'])
    app.add_url_rule('/logout', 'logout', auth_controller.logout)
    app.add_url_rule('/forget_password',
                     view_func=auth_controller.forget_password,
                     methods=['GET', 'POST'])
    app.add_url_rule('/create_account',
                     view_func=auth_controller.create_account,
                     methods=['GET', 'POST'])
    app.add_url_rule('/change_password',
                     view_func=user_controller.change_password,
                     methods=['GET', 'POST'])
    app.add_url_rule('/change_nickname',
                     view_func=user_controller.change_nickname,
                     methods=['GET', 'POST'])
    app.add_url_rule('/lobby', view_func=user_controller.lobby)
    app.add_url_rule('/lobby/train', view_func=user_controller.train)
    app.add_url_rule('/lobby/history', view_func=user_controller.history)
    app.add_url_rule('/lobby/game',
                     view_func=user_controller.game,
                     methods=['GET', 'POST'])
    app.add_url_rule('/game',
                     view_func=user_controller.game,
                     methods=['GET', 'POST'])
    app.add_url_rule('/game/move',
                     view_func=user_controller.move,
                     methods=['GET', 'POST'])
    app.add_url_rule('/game/suggest_move',
                     endpoint='suggest_move',
                     view_func=user_controller.suggest_move,
                     methods=['GET', 'POST'])
    from app.controllers.matchmaking_controller import match_bp
    app.register_blueprint(match_bp)
    from app.controllers.train_controller import train_bp
    app.register_blueprint(train_bp)

    from app.controllers.chat_controller import chat_bp
    app.register_blueprint(chat_bp)
