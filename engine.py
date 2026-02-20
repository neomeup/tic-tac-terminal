'''
engine should handle the board state and game logic - possible expansion for game logic when different win conditions
are introduced. i.e. win with a square as opposed to a line
'''

import random

## Build a grid that can be used interchangably with all game modes
def board_lst_build(size) -> list :
    # initial board positions creation
    board_lst = []
    for x in range(size):
        board_lst.append(list(range(size)))

    # Initial board ownership defined 
    for x in board_lst:
        for b in x:
            item = None
            x[b] = item
    return board_lst


## Determine a random starting player
def whose_turn() -> bool:
    turn_val = random.randint(0,1)
    if turn_val == 0:
        return True
    elif turn_val == 1:
        return False


## Identify where a player is on the board and if they can select, allow selections
def board_list_select(player_1_turn: bool, player_coordinates: list, board_lst: list[list]) -> tuple[list, bool] :

    changed_flag = False

    # Set Cell coordinates within board list
    y, x = player_coordinates
    working_cell = board_lst[y][x]

    if working_cell is None:
        if player_1_turn:
            working_cell = 0
        else:
            working_cell = 1
        changed_flag = True

    return board_lst, changed_flag
