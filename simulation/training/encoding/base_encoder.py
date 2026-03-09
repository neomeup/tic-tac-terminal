'''
Base class for board state encoders.

Requires derived classes to implement compute_encode.
'''

class BaseEncoder:
    
    def __init__(self, config):
        self.config = config
        
    def compute_encode(self, board_state, player_id):
        raise NotImplementedError