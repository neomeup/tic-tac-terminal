class BaseReward:

    def compute(self, player_id, winner, draw, board_state=None, move=None):
        raise NotImplementedError