'''
Represents the current game state.

Tracks:
- Board layout
- Current player
- Turn number
- Game completion flags (is_finished)

Used by simulation/sim_engine in:
_initialize_run_context
_choose_action
_step
'''

class GameState:
    def __init__(self, board, players, config):
        self.board = board
        self.players = players
        self.config = config

        self.current_player_id = players[0]
        self.turn_number = 0
        self.is_finished = False