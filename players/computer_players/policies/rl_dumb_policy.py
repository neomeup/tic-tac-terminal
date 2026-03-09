from core.move import Move
from players.computer_players.policies.base_policy import BasePolicy


class RLDumbPolicy(BasePolicy):

    def __init__(self):
        self.q_table = {}

    def _board_to_key(self, board):
        return str([[None if c is None else c.owner_id for c in row] for row in board])

    def select_action(self, player_id, board, config, rng):

        board_key = self._board_to_key(board)

        # Exploration vs exploitation
        if rng.random() < 0.3 or board_key not in self.q_table:
            return self._random_move(player_id, board, rng)

        return self._best_known_move(player_id, board, board_key, rng)

    def _random_move(self, player_id, board, rng):

        empty_positions = [
            (r, c)
            for r, row in enumerate(board)
            for c, cell in enumerate(row)
            if cell is None
        ]

        r, c = rng.choice(empty_positions)

        return Move(player_id=player_id, target_row=r, target_col=c)

    def _best_known_move(self, player_id, board, board_key, rng):
        # For now just fallback to random move
        return self._random_move(player_id, board, rng)

    def update(self, experience):
        # Placeholder for learning update
        pass