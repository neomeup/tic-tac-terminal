'''
Reward function built for q learning in tic tac toe style game 
'''


from debugging_testing.printing_debug import dbprint
from simulation.rewards.infra.base_reward import BaseReward

class QLearnTicTac(BaseReward):
    
    def __init__(self):

        debug_print = True
        self.dbprint = lambda *args, **kwargs: dbprint(debug_print, *args, **kwargs)

    def build_all_lines_with_coordinates(self, board_lst, win_length):
        
        win_length = win_length
        size = len(board_lst)

        def build_rows(board_lst) -> list:
            row_lst = []
            for row_index, row in enumerate(board_lst):
                row_with_coordinates = []
                for item_index, item in enumerate(row):
                    row_with_coordinates.append((row_index, item_index, item))
                if len(row_with_coordinates) >= win_length:
                    row_lst.append(row_with_coordinates)
            return row_lst
        
        def build_columns(board_lst):
            column_lst = []
            for col_index in range(size):
                column_with_coordinates = []
                for row_index in range(size):
                    column_with_coordinates.append((row_index, col_index, board_lst[row_index][col_index]))
                if len(column_with_coordinates) >= win_length:
                    column_lst.append(column_with_coordinates)
            return column_lst

        def build_diagonals(board_lst) -> list:
            diagonal_lst = []
            for diag_index in range(size):
                diagonal_rows = []
                row = 0
                column = diag_index
                while row < size and column < size:
                    diagonal_rows.append((row, column, board_lst[row][column]))
                    row += 1
                    column += 1
                if len(diagonal_rows) >= win_length:
                    diagonal_lst.append(diagonal_rows)

            for diag_index in range(1, size):
                diagonal_columns = []
                row = diag_index
                column = 0
                while row < size and column < size:
                    diagonal_columns.append((row, column, board_lst[row][column]))
                    row += 1
                    column += 1
                if len(diagonal_columns) >= win_length:
                    diagonal_lst.append(diagonal_columns)
                
            for anti_diag_index in range(size - 1, 0, -1):
                anti_diagonal_rows = []
                row = 0
                column = anti_diag_index
                while row < size and column >= 0:
                    anti_diagonal_rows.append((row, column, board_lst[row][column]))
                    row += 1
                    column -= 1
                if len(anti_diagonal_rows) >= win_length:
                    diagonal_lst.append(anti_diagonal_rows)
                
            for anti_diag_index in range(1, size):
                anti_diagonal_columns = []
                row = anti_diag_index
                column = size - 1
                while row < size and column >= 0:
                    anti_diagonal_columns.append((row, column, board_lst[row][column]))
                    row += 1
                    column -= 1
                if len(anti_diagonal_columns) >= win_length:
                    diagonal_lst.append(anti_diagonal_columns)
            
            return diagonal_lst

        rows = build_rows(board_lst)
        columns = build_columns(board_lst)
        diagonals = build_diagonals(board_lst)
  

        all_lines = rows + columns + diagonals   

        return all_lines

    def is_first_move(self, board_state):
        filled = sum(
            1 for row in board_state for col in row if col is not None
        )
        if filled == 1:
            return True
        return False
    
    def center_available(self, board):
        size = len(board)
        center = size // 2

        if board[center][center] is None:
            return True
        
        return False
    
    def center_move(self, board, move, reward, first_move):
        size = len(board)
        center = size // 2

        if move.target_row == center and move.target_col == center:
            reward += 0.3
            if not first_move:
                reward += 0.05
            return reward
        
        reward -= 0.1
        if first_move:
            reward -= 0.05
        return reward


    def one_away_from_win(self, board_state, player_id, all_lines, move, win_length):
        all_lines
        reward = 0

        one_away = win_length - 1

        for line in all_lines:
            player_count = sum(1 for cell in line if cell[2] is not None and cell[2].owner_id == player_id)
            empty_count = sum(1 for cell in line if cell[2] is None)

            if player_count == one_away and empty_count == 1:
                if any(r == move.target_row and c == move.target_col for (r, c, _) in line):
                    reward += 0.4

        return reward    

    def block_win(self, board_state, player_id, all_lines, move):
        all_lines
        reward = 0

        one_away = len(board_state) - 1

        for line in all_lines:
            oppenent_count = sum(1 for cell in line if cell[2] is not None and cell[2].owner_id != player_id)
            
            blocked = sum(1 for cell in line if cell[2].owner_id != player_id)

            if oppenent_count == one_away and blocked:
                pass

    def possible_win_line():
        pass









    def compute_reward(self, player_id, winner, draw, board_state, move, config):
        self.dbprint("start reward computation")
        self.dbprint("Player turn: ", player_id)
        self.dbprint("board state:", board_state)
        self.dbprint("move:", move)

        win_length = config.win_length
        all_lines = self.build_all_lines_with_coordinates(board_state, win_length)

        # Initialize reward
        reward = 0

        if self.is_first_move(board_state):
            first_move = True
            reward = self.center_move(board_state, move, reward, first_move)
        elif self.center_available(board_state):
            first_move = False
            reward = self.center_move(board_state, move, reward, first_move)


        reward += self.one_away_from_win(board_state, player_id, all_lines, move, win_length)

        # Game over conditions
        if (draw and winner is not None) or (not draw and winner):
            if draw:
                reward = 0.2
                return reward
                    
            if winner == player_id:
                reward = 1
                return reward
            
            # Should be set retroactively by sim engine as this case should never exist within reward engine
            if winner != player_id:
                reward = -1
                return reward
        
        self.dbprint("end reward computation")

        return reward