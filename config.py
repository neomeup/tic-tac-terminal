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

        # Human player flag and count
        self.human_player_exists: bool = True
        self.how_many_human: int = 2

        # Start conditions for movement
        self.random_start = True