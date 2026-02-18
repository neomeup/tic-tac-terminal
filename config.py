from dataclasses import dataclass

@dataclass
class GameConfig:
    x_char: str = "X"
    o_char: str = "O"
    empty_char: str = "-"
    board_size: int = 4
    win_length: int = 3