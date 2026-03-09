class BaseEncoder:
    
    def __init__(self, config):
        self.config = config
        
    def compute_encode(self, board_state, player_id):
        raise NotImplementedError