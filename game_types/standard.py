'''
Standard Tic-Tac-Toe rule implementation.

Checks:
- Win conditions
- Draw conditions
- Returns flags (won, winner, draw)
'''

def standard_rules(config, board_lst: list[list]) -> tuple[bool, int | None, bool]:
    
    win_length = config.win_length
    size = config.board_size
    total_players = len(config.player_types)

    # Win helper
    def consecutive_cells(cells_to_check: list, player_index: int, win_length: int) -> bool:
        cell_count = 0
        for cell in cells_to_check:
            if cell is not None and cell.owner_id == player_index:
                cell_count += 1
                if cell_count == win_length:
                    return True
            else:
                cell_count = 0
        return False
    
    # Stalemate helper
    def possible_line(cells_to_check: list, player_index: int, win_length: int):
        count = 0
        for cell in cells_to_check:
            if cell is None or (cell is not None and cell.owner_id == player_index):
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
        for diag_index in range(size):
            diagonal_rows = []
            row = 0
            column = diag_index
            while row < size and column < size:
                diagonal_rows.append(board_lst[row][column])
                row += 1
                column += 1
            diagonal_lst.append(diagonal_rows)

        for diag_index in range(1, size):
            diagonal_columns = []
            row = diag_index
            column = 0
            while row < size and column < size:
                diagonal_columns.append(board_lst[row][column])
                row += 1
                column += 1
            diagonal_lst.append(diagonal_columns)
            
        for anti_diag_index in range(size - 1, 0, -1):
            anti_diagonal_rows = []
            row = 0
            column = anti_diag_index
            while row < size and column >= 0:
                anti_diagonal_rows.append(board_lst[row][column])
                row += 1
                column -= 1
            diagonal_lst.append(anti_diagonal_rows)
            
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
        for player_index in range(total_players):
            if consecutive_cells(cells, player_index, win_length) is True:
                return True, player_index, False

    # Draw Checking
    for cells in all_lines:
        for player_index in range(total_players):
            if possible_line(cells, player_index, win_length):
                return False, None, False    
    

    return False, None, True