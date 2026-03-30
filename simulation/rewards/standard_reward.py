'''
Basic reward function.

- +1 for win
- 0 for draw
- -1 for loss
'''


from simulation.rewards.infra.base_reward import BaseReward

class StandardReward(BaseReward):

    def compute_reward(self, player_id, winner, draw, board_state=None, move=None, config=None):

        if draw:
            return 0.0
        
        if winner is None:
            return 0.0
        
        if winner == player_id:
            return 1.0
        
        if winner != player_id:
            return -1.0
        
        return ValueError("Reward miscalculation")