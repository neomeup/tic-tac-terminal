from dataclasses import dataclass

@dataclass
class GameConfig:
    def __init__(self):
        # Character for renders
        self.x_char: str = "X"
        self.o_char: str = "O"
        self.empty_char: str = "-"

        # Board and win settings
        self.board_size: int = 4
        self.win_length: int = 3 # Used for simple wins i.e. tic-tac-toe style

        # Optional render flag
        self.render: bool = True # Set False for non-rendered games

        # Optional key'ed input flag
        self.grab_keys: bool = True

        # Start conditions for movement
        self.random_start = True 