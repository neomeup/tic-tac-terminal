'''
Command-line human player input handler.

Processes keyboard movement and selection for CLI games. 
'''

from curses import KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT 

## Updates player position for human players and return it to main
def get_cli_move(key, current_player_index, player_position: list, size: int) -> list :

    player_id = current_player_index

    ## Player 1 movement (wasd)
    if key == ord("w"):
        if player_id == 0:
            player_position[0] = max((0, player_position[0] - 1))
    elif key == ord("s"):
        if player_id == 0:
            player_position[0] = min(((size-1), player_position[0] + 1))
    elif key == ord("a"):
        if player_id == 0:
            player_position[1] = max((0, player_position[1] - 1))
    elif key == ord("d"):
        if player_id == 0:
            player_position[1] = min(((size-1), player_position[1] + 1))


    ## Player 2 movement (arrows)
    elif key == KEY_UP:
        if player_id == 1:
            player_position[0] = max((0, player_position[0] - 1))
    elif key == KEY_DOWN:
        if player_id == 1:
            player_position[0] = min(((size-1), player_position[0] + 1))
    elif key == KEY_LEFT:
        if player_id == 1:
            player_position[1] = max((0, player_position[1] - 1))
    elif key == KEY_RIGHT:
        if player_id == 1:
            player_position[1] = min(((size-1), player_position[1] + 1))

    return player_position