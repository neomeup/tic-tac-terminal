import uuid
from datetime import datetime

class GameRunContext:
    def __init__(self, config):
        self.game_id = str(uuid.uuid4())
        self.config_snapshot = config
        self.start_time = datetime.utcnow()
        self.end_time = None
        self.winner = None

        self.moves = []  # list of move logs
        self.players = {}  # not sure if needed - come back to this

    def register_player(self, player_id, player_type, model_version=None):
        self.players[player_id] = {
            "player_type": player_type,
            "model_version": model_version
        }

    def log_move(self, turn_number, player_id, board_state, action, reward=None):
        self.moves.append({
            "turn_number": turn_number,
            "player_id": player_id,
            "board_state": board_state,
            "action": action,
            "reward": reward
        })

    def finalize(self, winner):
        self.winner = winner
        self.end_time = datetime.utcnow()