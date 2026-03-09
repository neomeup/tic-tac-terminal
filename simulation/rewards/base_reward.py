class BaseReward:

    def compute_reward(self, player_id, winner, draw, board_state=None, move=None):
        raise NotImplementedError