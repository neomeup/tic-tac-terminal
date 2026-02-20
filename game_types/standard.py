## Determine is game is over - based on tic-tac-toe style gameplay
def standard_rules(config, board_lst: list[list]) -> tuple[bool, bool, bool]:
    
    ##  All returns in following format -> won_game, player_1_win, drawn_game
    win_length = config.win_length
    size = config.board_size

    # Win helper
    # Helper function using win length to determine consecutive cells
    def consecutive_cells(cells_to_check: list, player_index: int, win_length: int) -> bool:
        cell_count = 0
        for cell in cells_to_check:
            if cell == player_index:
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
            if cell == player_index or cell is None:
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

    all_lines = rows + columns + diagonals

    # Win checking
    for cells in all_lines:
        if consecutive_cells(cells, 0, win_length) is True:
            return True, True, False
        elif consecutive_cells(cells, 1, win_length) is True:
            return True, False, False

    # Draw Checking
    for cells in all_lines:
        if possible_line(cells, 0, win_length) or possible_line(cells, 1, win_length):
           return False, False, False    
    

    return False, False, True # Returns a drawn game running state if no wins or possible wins are detected