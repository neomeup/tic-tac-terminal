class GameState:
    def __init__(self, board, players, config):
        self.board = board
        self.players = players
        self.config = config

        self.current_player_id = players[0]
        self.turn_number = 0
        self.is_finished = False