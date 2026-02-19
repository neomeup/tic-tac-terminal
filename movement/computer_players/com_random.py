'''
Random move algorithm for a computer player
'''
import random


def get_move(player_1_turn, board_lst, config) -> list:
    
    if player_1_turn:
        player_index = 0
    if not player_1_turn:
        player_index = 1

    # List of empty positions to grab one randomly
    empty_positions = []
    for row_index, row in enumerate(board_lst):
        for col_index, column in enumerate(row):
            if not column[0] and not column[1]:
                empty_cell = [row_index, col_index]
                empty_positions.append(empty_cell)

    # Pick a random empty cell
    row, col = random.choice(empty_positions)

    # Set working cell
    working_cell = board_lst[row][col]
    
    working_cell[player_index] = True

    updated_board_lst = board_lst
    return updated_board_lst