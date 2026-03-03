from dataclasses import dataclass

@dataclass
class Piece:
    owner_id: int
    piece_type: str