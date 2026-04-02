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
            draw_reward = 0.2
            reward = draw_reward
            return reward
        
        if winner == player_id:
            winner_reward = 1
            reward = winner_reward
            return reward
        
        if winner != player_id:
            loser_reward = -1
            reward = loser_reward
            return reward
        
        return ValueError("Reward miscalculation")