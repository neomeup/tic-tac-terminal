'''
Base class for AI policies.

Defines choose_move(board_state, player_id).
'''

class BasePolicy:

    def select_action(self, player_id, board, config, rng):
        raise NotImplementedError