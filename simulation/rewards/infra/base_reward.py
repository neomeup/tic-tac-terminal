'''
Base class for reward computation.

Custom reward schemes must implement compute_reward.
'''

class BaseReward:

    def compute_reward(self, player_id, winner, draw, board_state=None, move=None, config=None):
        raise NotImplementedError