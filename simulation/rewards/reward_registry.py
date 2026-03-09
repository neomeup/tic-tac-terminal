'''
Registry mapping of reward type names to reward classes.

Enables dynamic selection of reward computation logic.
'''

from simulation.rewards.standard_reward import StandardReward

reward_registry = {
    "standard": StandardReward
}