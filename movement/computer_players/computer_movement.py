'''
Computer movement middle man for main and registry
'''

from movement.computer_players.registry import computer_move_registry


def get_computer_move(player_1_turn, board_lst, config):
    player_index = 0 if player_1_turn else 1
    algorithm_name = config.computer_algorithms[player_index]
    move_function = computer_move_registry[algorithm_name]
    return move_function(player_1_turn, board_lst)