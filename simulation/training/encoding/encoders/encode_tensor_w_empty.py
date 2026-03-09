import numpy as np
from simulation.training.encoding.base_encoder import BaseEncoder

class TensorPlayersWithEmptyEncode(BaseEncoder):

    def compute_encode(self, board_state, player_id):

        size = len(board_state)

        player_quantity = len(self.config.player_types)

        tensor_w_empty = np.zeros((player_quantity + 1, size, size), dtype=np.float32)

        for row in range(size):
            for col in range(size):
                for x in range(player_quantity + 1):

                    cell = board_state[row][col]

                    if cell is None and x == player_quantity:
                        tensor_w_empty[x][row][col] = 1

                    elif cell is None:
                        tensor_w_empty[x][row][col] = 0

                    elif cell["owner"] == x:
                        tensor_w_empty[x][row][col] = 1
                    
                    else: 
                        tensor_w_empty[x][row][col] = 0

        return tensor_w_empty