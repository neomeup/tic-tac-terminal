'''
Random move algorithm for a computer player
'''
import random


def get_move(player_1_turn, board_lst) -> list:
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
    if player_1_turn:
        working_cell = 0
    else:
        working_cell = 1

    board_lst[row][col] = working_cell

    updated_board_lst = board_lst
    return updated_board_lst