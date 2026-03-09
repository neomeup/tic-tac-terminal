'''
Encodes board as a 2D vector.

- 1 for current player's cells
- -1 for opponent's cells
- 0 for empty cells
'''

import numpy as np
from simulation.training.encoding.base_encoder import BaseEncoder

class VectorEncode(BaseEncoder):

    def compute_encode(self, board_state, player_id):

        size = len(board_state)

        vector = np.zeros((size, size), dtype=np.float32)

        for row in range(size):
            for col in range(size):

                cell = board_state[row][col]

                if cell is None:
                    vector[row][col] = 0

                elif cell["owner"] == player_id:
                    vector[row][col] = 1

                elif cell["owner"] != player_id: 
                    vector[row][col] = -1

        return vector