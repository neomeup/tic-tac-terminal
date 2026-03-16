'''
Logs game metadata and moves during a single run.

Provides:
- Move logging
- Player registration
- Game finalization

Used by simulation/result in:
in __init__ as runs

simulation/sim_engine in:
_initialize_run_context - to initialize context and add player data
_run_single_game - logs first move
_step - to log all following moves

'''

import uuid
from datetime import datetime

class GameRunContext:
    def __init__(self, config):
        self.game_id = str(uuid.uuid4())
        self.config_snapshot = config
        self.start_time = datetime.utcnow()
        self.end_time = None
        self.winner = None
        self.draw = False
        
        self.moves = []  # list of move logs
        self.players = {}  # players log

    def register_player(self, player_id, player_type, model_version=None):
        self.players[player_id] = {
            "player_type": player_type,
            "model_version": model_version
        }

    def log_move(self, turn_number, player_id, board_state, action, reward=None, done=False):
        self.moves.append({
            "turn_number": turn_number,
            "player_id": player_id,
            "board_state": board_state,
            "action": action,
            "reward": reward,
            "done": done
        })

    def finalize(self, winner, draw):
        self.winner = winner
        self.draw = draw
        self.end_time = datetime.utcnow()