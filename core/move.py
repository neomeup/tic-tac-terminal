'''
Represents a player move.

Stores:
- player_id
- target row and column

Used by game_engine/apply_move in:
apply_move

All computer policies will return Move
'''

from dataclasses import dataclass

@dataclass
class Move:
    player_id: int
    target_row: int
    target_col: int