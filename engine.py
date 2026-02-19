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

    # bool flags to notate if a square has been selected by a player or not
    p1_selected = False
    p2_selected = False

    # addition of selection flags to board positions
    for x in board_lst:
        for b in x:
            item = [p1_selected, p2_selected, b]
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
def board_list_select(player_1_turn: bool, player_coordinates: list, board_lst: list[list[tuple[bool, bool, int]]]) -> tuple[list, bool] :
    if player_1_turn is True:
        non_active_player = 1 # Player two is inactive
        active_player = 0 # Player one is active - corresponds to bool flags within board list
    elif player_1_turn is False:
        non_active_player = 0 # Player one is inactive
        active_player = 1 # Player two is active - corresponds to bool flags within board list

    changed_flag = False

    # Set Cell coordinates within board list
    y, x = player_coordinates
    working_cell = board_lst[y][x]

    if working_cell[non_active_player] is True:
        pass
    elif working_cell[active_player] is False:
        working_cell[active_player] = True
        changed_flag = True

    return board_lst, changed_flag


## Determine is game is over - based on tic-tac-toe style gameplay
def game_finished(config, board_lst: list[list[tuple[bool, bool, int]]]) -> tuple[bool, bool, bool]:
    
    ##  All returns in following format -> won_game, player_1_win, drawn_game
    win_length = config.win_length
    size = config.board_size

    # Win helper
    # Helper function using win length to determine consecutive cells
    def consecutive_cells(cells_to_check: list, player_index: int, win_length: int) -> bool:
        cell_count = 0
        for cell in cells_to_check:
            if cell[player_index]:
                cell_count += 1
                if cell_count == win_length:
                    return True
            else:
                cell_count = 0
        return False
    
    # Stalemate helper
    # Helper function to return True if player could win the cells being checked
    def possible_line(cells_to_check: list, player_index: int, win_length: int):
        count = 0
        for cell in cells_to_check:
            if cell[player_index] or (not cell[0] and not cell[1]):
                count += 1
                if count >= win_length:
                    return True
            else:
                count = 0
        return False

    def build_rows(board_lst) -> list:
        row_lst = []
        for row in board_lst:
            row_lst.append(row)
        return row_lst


    def build_columns(board_lst) -> list:
        column_lst = []
        for col_index in range(size):
            column = [board_lst[row][col_index] for row in range(size)]
            column_lst.append(column)
        return column_lst
    

    def build_diagonals(board_lst) -> list:
        diagonal_lst = []
        # Moving row-wise
        for diag_index in range(size):
            diagonal_rows = []
            row = 0
            column = diag_index
            while row < size and column < size:
                diagonal_rows.append(board_lst[row][column])
                row += 1
                column += 1
            diagonal_lst.append(diagonal_rows)

        # Move column wise
        for diag_index in range(1, size): # Readability - possible to start at 1 due to initial diagonal already being checked in row-wise
            diagonal_columns = []
            row = diag_index
            column = 0
            while row < size and column < size:
                diagonal_columns.append(board_lst[row][column])
                row += 1
                column += 1
            diagonal_lst.append(diagonal_columns)
            
        # Move row wise
        for anti_diag_index in range(size - 1, 0, -1):
            anti_diagonal_rows = []
            row = 0
            column = anti_diag_index
            while row < size and column >= 0:
                anti_diagonal_rows.append(board_lst[row][column])
                row += 1
                column -= 1
            diagonal_lst.append(anti_diagonal_rows)
            
        # Move column wise
        for anti_diag_index in range(1, size):
            anti_diagonal_columns = []
            row = anti_diag_index
            column = size - 1
            while row < size and column >= 0:
                anti_diagonal_columns.append(board_lst[row][column])
                row += 1
                column -= 1
            diagonal_lst.append(anti_diagonal_columns)
        
        return diagonal_lst


    rows = build_rows(board_lst)
    columns = build_columns(board_lst)
    diagonals = build_diagonals(board_lst)


    # Win checking
    for cells in rows:
        if consecutive_cells(cells, 0, win_length) is True:
            return True, True, False
        if consecutive_cells(cells, 1, win_length) is True:
            return True, False, False

    for cells in columns:
        if consecutive_cells(cells, 0, win_length) is True:
            return True, True, False
        if consecutive_cells(cells, 1, win_length) is True:
            return True, False, False

    for cells in diagonals:
        if consecutive_cells(cells, 0, win_length) is True:
            return True, True, False
        if consecutive_cells(cells, 1, win_length) is True:
            return True, False, False


    # Draw Checking
    for cells in rows:
        if possible_line(cells, 0, win_length) or possible_line(cells, 1, win_length):
           return False, False, False
    
    for cells in columns:
        if possible_line(cells, 0, win_length) or possible_line(cells, 1, win_length):
           return False, False, False

    for cells in diagonals:
        if possible_line(cells, 0, win_length) or possible_line(cells, 1, win_length):
           return False, False, False       
    

    return False, False, True # Returns a game running state if no wins or draws are detected


