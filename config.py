'''
Defines global configuration for the Tic-Tac-Toe game.

'''

from dataclasses import dataclass
from typing import Literal

@dataclass
class GameConfig:
    board_size: int = 3 # Board size

    # Character for renders, can be any single character
    x_char: str = "X"
    o_char: str = "O"
    empty_char: str = "-"

    win_length: int = 3 # Win length Tic-tac-toe/standard rule set

    # Game type indicator
    rule_set: str = "standard" # registerized in game_types/rules_registry
    '''
    - individually should be used as win/draw verification
    - logic ties to apply_move which checks for a valid move thus this should be changed if play rules change i.e. captures
    '''


    # Piece type
    piece_type: str = "standard_x-o" # Could be registerized if you want multiple piece types - would be tied to rules


    random_start: bool = True # Start conditions for movement
    random_seed: int | None = None # Random Seed Config
    
    render: bool = False # Optional render flag
    render_type: str = "cli" # Registerized in players/human_players/regsitry for selected type of movement for human players
    ## render_type is hardcoded for renderring in main.  If additional render types are built, this should be changed
    ## again, render_type is tied to movement for human players as well though

    # Persistence
    mongo_logging_enabled: bool = True
    postgres_logging_enabled: bool = True

    model_storage_local_pre_base_path = "players/computer_players/model_storage/data"
    model_storage_backend: Literal["local", "s3", None] = "local"

    # Training Enablement
    online_training_enabled: bool = False
    offline_training_enabled: bool = False

    # Games to be played in simulation mode
    how_many_games: int = 1
    
    state_encoding_dim_type: str = "tensor_with_empty" # registerized in simulation/training/encoding/encoder_registry
    state_encoding_flattened: bool = True # interacts with dim type to provide a flat version of the selected type
    
    # Offline training agent/reward types
    offline_agent: str = "rl_dumb_agent" # registerized in players/computer_players/agent_registry
    offline_reward_type: str = "standard" # registerized in simulation/rewards/reward_registry
    
    # Online training and player type list - player types must be config'd for all games even without training
    online_reward_type: str = "standard" # registerized in simulation/rewards/reward_registry
    def __post_init__(self):
        self.player_types: list[Literal["human", "computer"]] = ["computer", "computer"]

        # If computer player type please input policy and agent type
        self.policy_type: list = ["rl_dumb_policy", "random_policy"] #registerized in players/computer_players/model_policy_registry
        self.agent_type: list = ["rl_dumb_agent", "random_agent"] # registerized in players/computer_players/agent_registry
        self.model_version: list = ["v1", "v1"]