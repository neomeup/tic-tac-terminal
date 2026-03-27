'''
Wrapper between computer player moves and main game logic.
'''

from simulation.rewards.infra.reward_registry import reward_registry


def get_reward_class(player_id, config):

    reward_type = config.reward_type[player_id]

    reward_class = reward_registry[reward_type]

    return reward_class


def get_reward(player_id, winner, draw, config, board_state, move):

    reward_class = get_reward_class(player_id, config)

    reward_instance = reward_class()

    return reward_instance.compute_reward(player_id, winner, draw, board_state, move)