import numpy as np
from simulation.training.encoding.base_encoder import BaseEncoder

class TensorPlayersEncode(BaseEncoder):

    def compute_encode(self, board_state, player_id):

        size = len(board_state)

        player_quantity = len(self.config.player_types)

        tensor_players = np.zeros((player_quantity, size, size), dtype=np.float32)

        for row in range(size):
            for col in range(size):
                for x in range(player_quantity):

                    cell = board_state[row][col]

                    if cell is None or cell["owner"] != x:
                        tensor_players[x][row][col] = 0
                    
                    elif cell["owner"] == x:
                        tensor_players[x][row][col] = 1

        return tensor_players.flatten(), tensor_players