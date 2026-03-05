'''
Registry for the different algorithms 
'''

from movement.computer_players.policies.random_policy import RandomPolicy
from movement.computer_players.policies.rl_dumb_policy import RLDumbPolicy

model_policy_registry = {
    "random_policy": RandomPolicy,
    "rl_dumb_policy": RLDumbPolicy,
}