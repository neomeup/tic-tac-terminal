'''
Registry mapping of reward type names to reward classes.

Enables dynamic selection of reward computation logic.
'''

from simulation.rewards.standard_reward import StandardReward
from simulation.rewards.q_learning_tic_tac_reward import QLearnTicTac

reward_registry = {
    "standard": StandardReward,
    "qlearn_tic_tac": QLearnTicTac
}