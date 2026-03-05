'''
Registry for the different algorithms 
'''

from movement.computer_players.policies.random_policy import get_move as random_move
from movement.computer_players.agents.rl_dumb_agent import get_move as rl_dumb_move

computer_model_registry = {
    "random": random_move,
    "rl_dumb": rl_dumb_move,
}