'''
Random move policy for AI players.

Selects a valid move at random.
'''
from core.move import Move
from players.computer_players.policies.base_policy import BasePolicy


class ReverseSequencePolicy(BasePolicy):

    def select_action(self, current_player_index: int, board_lst: list[list], config, rng, encoded_state=None) -> list:
        
        id = current_player_index
        

        # Force central move as first move - testing
        force_center = False

        if force_center:
            size = len(board_lst)
            center = size // 2

            if board_lst[center][center] is None:
                r = center
                c = center
                return Move (player_id=id, target_row=r, target_col=c)
        

        for row_index, row in reversed(list(enumerate(board_lst))):
            for col_index, cell in reversed(list(enumerate(row))):
                
                if cell is None:
                    r=row_index
                    c=col_index
                               
                    return Move (player_id=id, target_row=r, target_col=c)
        
        # Should never get to this.
        raise ValueError("No valid moves")