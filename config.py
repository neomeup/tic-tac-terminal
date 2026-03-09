from dataclasses import dataclass

@dataclass
class GameConfig:
    # Board size
    board_size: int = 3


    # Character for renders
    x_char: str = "X"
    o_char: str = "O"
    empty_char: str = "-"
    # Win length Tic-tac-toe/standard rule sets
    win_length: int = 3 # Used for simple wins i.e. tic-tac-toe style


    # Game type indicator
    rule_set: str = "standard" # registerized
    # Piece type
    piece_type: str = "standard_x-o" # Could be registerized if you want multiple piece types - would be tied to rules


    # Start conditions for movement
    random_start: bool = True
    # Random Seed Config
    random_seed: int | None = None


    # Optional render flag
    render: bool = False
    render_type: str = "cli" # Could be registerized if you want multiple render types
    # Games to be played in simulation mode
    how_many_games: int = 1



    # Online training within SimEngine bools
    online_training_enabled: bool = True
    offline_training_enabled: bool = True
    
    offline_agent: str = "rl_dumb_agent"

    reward_type: str = "standard" #registerized
    state_encoding_flattened: bool = False # interacts with dim type to provide a flat version of the selected type
    state_encoding_dim_type: str = "vector" # registerized

    def __post_init__(self):
        # Player types
        self.player_types: list = ["computer", "computer"] #registerized
        self.model_type: list = ["rl_dumb_policy", "random_policy"] #registerized
        self.agent_type: list = ["rl_dumb_agent", "random_agent"] # registerized