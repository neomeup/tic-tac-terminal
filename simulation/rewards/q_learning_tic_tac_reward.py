'''
Reward function built for q learning in tic tac toe style game 
'''




from simulation.rewards.infra.base_reward import BaseReward

class QLearnTicTac(BaseReward):
    
    def compute_reward(self, player_id, winner, draw, board_state=None, move=None):

        if draw:
            return 0.0
        
        if winner is None:
            return 0.0
        
        if winner == player_id:
            return 1.0
        
        if winner != player_id:
            return -1.0
        
        return ValueError("Reward miscalculation")