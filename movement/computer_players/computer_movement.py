'''
Computer movement middle man for main and registry
'''

from movement.computer_players.registry import computer_model_registry

# Should return a move object
def get_computer_move(current_player_index, board_lst, config):
    player_index = current_player_index
    algorithm_type = config.model_type[player_index]
    move_function = computer_model_registry[algorithm_type]
    return move_function(current_player_index, board_lst, config)