'''
Movement for human players 
'''

from curses import KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT
from engine.player_utils import get_player_id

## Updates player position for human players and return it to main
def get_player_move(key, player_1_turn: bool, player_position: list, size: int) -> list :

    player_id = get_player_id(player_1_turn)

    ## Player 1 movement (wasd)
    if key == ord("w"): #key up
        if player_id == 0: # Isolate movement by player turn for player 1
            player_position[0] = max((0, player_position[0] - 1))
    elif key == ord("s"): #key down
        if player_id == 0:
            player_position[0] = min(((size-1), player_position[0] + 1))
    elif key == ord("a"): #key left
        if player_id == 0:
            player_position[1] = max((0, player_position[1] - 1))
    elif key == ord("d"): #key right
        if player_id == 0:
            player_position[1] = min(((size-1), player_position[1] + 1))


    ## Player 2 movement (arrows)
    elif key == KEY_UP: #key up
        if player_id == 1: # Isolate movement by player turn for player 2
            player_position[0] = max((0, player_position[0] - 1))
    elif key == KEY_DOWN: #key down
        if player_id == 1:
            player_position[0] = min(((size-1), player_position[0] + 1))
    elif key == KEY_LEFT: #key left
        if player_id == 1:
            player_position[1] = max((0, player_position[1] - 1))
    elif key == KEY_RIGHT: #key right
        if player_id == 1:
            player_position[1] = min(((size-1), player_position[1] + 1))

    return player_position