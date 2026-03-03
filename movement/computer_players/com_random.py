'''
Random move algorithm for a computer player
'''
import random
from core.move import Move

def get_move(current_player_index: int, board_lst: list[list], config) -> list:
    # List of empty positions to grab one randomly
    empty_positions = []
    for row_index, row in enumerate(board_lst):
        for col_index, cell in enumerate(row):
            if cell is None:
                empty_cell = [row_index, col_index]
                empty_positions.append(empty_cell)

    # Pick a random empty cell
    row, col = random.choice(empty_positions)

    return Move (player_id=current_player_index, target_row=row, target_col=col)