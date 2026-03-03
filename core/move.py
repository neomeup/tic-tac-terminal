from dataclasses import dataclass

@dataclass
class Move:
    player_id: int
    target_row: int
    target_col: int