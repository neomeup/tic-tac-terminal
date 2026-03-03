'''
Random move algorithm for a computer player
'''
import random
from core.piece import Piece
from engine.player_utils import get_player_id


def get_move(player_1_turn, board_lst, config) -> list:
    # List of empty positions to grab one randomly
    empty_positions = []
    for row_index, row in enumerate(board_lst):
        for col_index, cell in enumerate(row):
            if cell is None:
                empty_cell = [row_index, col_index]
                empty_positions.append(empty_cell)

    # Pick a random empty cell
    row, col = random.choice(empty_positions)

    # Assign working cell
    player_id = get_player_id(player_1_turn)

    

    board_lst[row][col] = Piece(
        owner_id=player_id,
        piece_type=config.piece_type
    )

    updated_board_lst = board_lst
    return updated_board_lst