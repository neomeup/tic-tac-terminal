'''
engine should handle the board state and game logic - possible expansion for game logic when different win conditions
are introduced. i.e. win with a square as opposed to a line
'''

from core.piece import Piece

## Build a grid that can be used interchangably with all game modes
def build_starting_board(size) -> list :
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


## Identify where a player is on the board and if they can select, allow selections
def board_list_select(current_player_index: int, player_coordinates: list, board_lst: list[list], config) -> tuple[list, bool] :

    changed_flag = False

    # Set Cell coordinates within board list
    y, x = player_coordinates
    working_cell = board_lst[y][x]

    if working_cell is None:
        player_id = current_player_index
    
        working_cell = Piece(
            owner_id=player_id,
            piece_type=config.piece_type
        )

        changed_flag = True

    board_lst[y][x] = working_cell
    return board_lst, changed_flag
