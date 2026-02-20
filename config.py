from dataclasses import dataclass

@dataclass
class GameConfig:
    def __init__(self):
        # Character for renders
        self.x_char: str = "X"
        self.o_char: str = "O"
        self.empty_char: str = "-"

        # Board size
        self.board_size: int = 3

        # Win length Tic-tac-toe/standard rule sets
        self.win_length: int = 3 # Used for simple wins i.e. tic-tac-toe style

        # Game type indicator
        self.rule_set: str = "standard"

        # Optional render flag
        self.render: bool = True # Set False for non-rendered games

        # Player types
        self.player_types: list = ["human", "computer"] # ["human", "computer"] -> will yeild single player mode
        # If computer player what algorithm to use
        self.computer_algorithms: list = ["random", "random"]

        # Start conditions for movement
        self.random_start: bool = True

        # Games to be played in computer only mode
        self.how_many_games: int = 2