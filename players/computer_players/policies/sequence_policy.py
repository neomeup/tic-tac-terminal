'''
Random move policy for AI players.

Selects a valid move at random.
'''
from core.move import Move
from players.computer_players.policies.base_policy import BasePolicy


class SequencePolicy(BasePolicy):
    def select_action(self, current_player_index: int, board_lst: list[list], config, rng) -> list:
        
        id = current_player_index

        for row_index, row in enumerate(board_lst):
            for col_index, cell in enumerate(row):
                
                if cell is None:
                    r=row_index
                    c=col_index
                               
                    return Move (player_id=id, target_row=r, target_col=c)
        
        # Should never get to this.
        raise ValueError("No valid moves")