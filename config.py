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
        self.render: bool = False # Set False for non-rendered games
        self.render_type: str = "cli"

        # Player types
        self.player_types: list = ["computer", "computer", "computer"] # ["human", "computer"] -> will yeild single player mode
        self.model_type: list = ["random", "random", "random"]

        # Piece type
        self.piece_type: str = "standard_x-o"

        # Start conditions for movement
        self.random_start: bool = True

        # Games to be played in simulation mode
        self.how_many_games: int = 2

        # Random Seed Config
        self.random_seed: int | None = None