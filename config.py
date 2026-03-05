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
    render: bool = False
    render_type: str = "cli" #registerized

    # Piece type
    piece_type: str = "standard_x-o"

    # Start conditions for movement
    random_start: bool = True

    # Games to be played in simulation mode
    how_many_games: int = 2

    # Random Seed Config
    random_seed: int | None = None

    # Online training within SimEngine bool
    online_training_enabled: bool = True

    def __post_init__(self):
        # Player types
        self.player_types: list = ["computer", "computer"] #registerized
        self.model_type: list = ["rl_dumb", "random"] #registerized