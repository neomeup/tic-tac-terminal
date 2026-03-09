'''
Represents a game piece on the board.

Tracks ownership and other piece-specific properties.
'''
from dataclasses import dataclass

@dataclass
class Piece:
    owner_id: int
    piece_type: str