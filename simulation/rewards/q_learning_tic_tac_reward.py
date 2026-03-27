'''
Reward function built for q learning in tic tac toe style game 
'''


from debugging_testing.printing_debug import dbprint
from simulation.rewards.infra.base_reward import BaseReward

class QLearnTicTac(BaseReward):
    
    def __init__(self):

        debug_print = True
        self.dbprint = lambda *args, **kwargs: dbprint(debug_print, *args, **kwargs)

    def build_all_lines(self, board_lst):
        
        size = len(board_lst)

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

        return all_lines

    def is_first_move(self, board_state):
        filled = sum(
            1 for row in board_state for col in row if col is not None
        )
        if filled == 1:
            return True
        return filled == 1
    
    def center_available(self, board):
        size = len(board)
        center = size // 2

        if board[center][center] is None:
            return True
        
        return False
    
    def center_move(self, board, move, reward):
        size = len(board)
        center = size // 2

        if move.target_row == center and move.target_col == center:
            self.dbprint("first move centered")
            reward =+ 0.3 
            return reward
        
        reward -= 0.1
        return reward



    def one_away_from_win(self, board_state, player_id, all_lines):
        all_lines
        reward = 0

        one_away = len(board_state) - 1

        for line in all_lines:
            player_count = sum(1 for cell in line if cell is not None and cell.owner_id == player_id)
            empty_count = sum(1 for cell in line if cell is None)

            
            if player_count == one_away and empty_count == 1:
                reward = 0.5

        return reward    












    def compute_reward(self, player_id, winner, draw, board_state, move):
        self.dbprint("start reward computation")
        self.dbprint("Player turn: ", player_id)
        all_lines = self.build_all_lines(board_state)
        self.dbprint("board state:", board_state)
        self.dbprint("move:", move)
        
        # Initialize reward
        reward = 0

        if self.is_first_move(board_state):
            self.dbprint("first move")
            reward = self.center_move(board_state, move, reward)
        elif self.center_available(board_state):
            reward = self.center_move(board_state, move, reward)


        reward += self.one_away_from_win(board_state, player_id, all_lines)

        # Game over conditions
        if draw and winner is not None:
            if draw:
                reward = 0.2
                return reward
                    
            if winner == player_id:
                reward = 1
                return reward
            
            if winner != player_id:
                reward = -1
                return reward
        
        self.dbprint("end reward computation")

        return reward