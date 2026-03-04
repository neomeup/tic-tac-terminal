from dataclasses import dataclass

@dataclass
class GameConfig:
    # Character for renders
    x_char: str = "X"
    o_char: str = "O"
    empty_char: str = "-"

    # Board size
    board_size: int = 3

    # Win length Tic-tac-toe/standard rule sets
    win_length: int = 3 # Used for simple wins i.e. tic-tac-toe style

    # Game type indicator
    rule_set: str = "standard"

    # Optional render flag
    render: bool = False # Set False for non-rendered games
    render_type: str = "cli"

    # Piece type
    piece_type: str = "standard_x-o"

    # Start conditions for movement
    random_start: bool = True

    # Games to be played in simulation mode
    how_many_games: int = 3

    # Random Seed Config
    random_seed: int | None = 15

    def __post_init__(self):
        # Player types
        self.player_types: list = ["computer", "computer", "computer"] # ["human", "computer"] -> will yeild single player mode
        self.model_type: list = ["random", "random", "random"]