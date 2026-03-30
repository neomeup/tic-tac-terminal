'''
Base class for AI policies.

Defines choose_move(board_state, player_id).
'''

from core.move import Move
from players.computer_players.policies.base_policy import BasePolicy


class PlannedGame(BasePolicy):

    def is_x_move(self, board_state, x_move):
        x = x_move - 1

        filled = sum(
            1 for row in board_state for col in row if col is not None
        )
        if filled == x:
            return True
        return False

    def select_action(self, current_player_index: int, board_lst: list[list], config, rng, encoded_state=None):
        
        player_id = current_player_index


        first_move = self.is_x_move(board_lst, x_move = 1)
        #second_move = self.is_x_move(board_lst, x_move = 2)
        third_move = self.is_x_move(board_lst, x_move = 3)
        #fourth_move = self.is_x_move(board_lst, x_move = 4)
        fifth_move = self.is_x_move(board_lst, x_move = 5)
        #sixth_move = self.is_x_move(board_lst, x_move = 6)
        seventh_move = self.is_x_move(board_lst, x_move = 7)
        #eigth_move = self.is_x_move(board_lst, x_move = 8)
        ninth_move = self.is_x_move(board_lst, x_move = 9)


        if first_move:
            r = 1
            c = 1
            if board_lst[r][c] is None:
                return Move (player_id=player_id, target_row=r, target_col=c)
            
        if third_move:
            r = 1
            c = 2
            if board_lst[r][c] is None:
                return Move (player_id=player_id, target_row=r, target_col=c)

        if fifth_move:
            r = 0
            c = 0
            if board_lst[r][c] is None:
                return Move (player_id=player_id, target_row=r, target_col=c)

        if seventh_move:
            r = 2
            c = 1
            if board_lst[r][c] is None:
                return Move (player_id=player_id, target_row=r, target_col=c)

        if ninth_move:
            r = 2
            c = 0
            if board_lst[r][c] is None:
                return Move (player_id=player_id, target_row=r, target_col=c)   

         

        for row_index, row in reversed(list(enumerate(board_lst))):
            for col_index, cell in reversed(list(enumerate(row))):
                
                if cell is None:
                    r=row_index
                    c=col_index
                               
                    return Move (player_id=player_id, target_row=r, target_col=c)


        return Move (player_id=player_id, target_row=r, target_col=c)