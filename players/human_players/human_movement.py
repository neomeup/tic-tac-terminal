'''
Translates key presses into player moves.

Supports arrow keys, WASD, and enter/select keys.
'''

from players.human_players.registry import human_move_registry

def get_player_move(key, current_player_index, player_position: list, size: int, config):
    human_input_type = config.render_type
    move_function = human_move_registry[human_input_type]
    return move_function(key, current_player_index, player_position, size)