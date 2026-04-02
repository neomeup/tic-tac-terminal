'''
Defines base class for configs

'''

from dataclasses import dataclass
from typing import Literal, Optional

@dataclass
class GameConfig:

    # Core game
    board_size: int
    x_char: str
    o_char: str
    empty_char: str
    win_length: int # Win length Tic-tac-toe/standard rule set

    ## - individually should be used as win/draw verification
    ## - logic ties to apply_move which checks for a valid move thus this should be changed if play rules change i.e. captures
    rule_set: str # registerized in game_types/rules_registry
    piece_type: str # Could be registerized if you want multiple piece types - would be tied to rules


    '''----------------------------------'''
    # Random runtime 
    random_start: bool # Start conditions for movement
    random_seed: Optional[int | None] # Random Seed Config


    '''----------------------------------'''
    # Rendered runtime
    render: bool

    ## render_type is hardcoded for renderring in main.  If additional render types are built, this should be changed
    ## render_type is tied to movement for human players as well thus is changed this should change as well
    render_type: str # Registerized in players/human_players/regsitry for selected type of movement for human players


    '''----------------------------------'''
    # Debugging
    debug_prints_enabled: bool
    debug_print_frequency_offline_batch: int
    debug_print_frequency_TransitionsSteps: int

    # Timing
    timing: bool


    '''----------------------------------'''
    # Persistence
    mongo_logging_enabled: bool
    postgres_logging_enabled: bool

    model_storage_local_pre_base_path: str
    model_storage_backend: Literal["local", "s3", None]

    model_checkpoint_enabled: bool
    model_checkpoint_interval: int # steps 
    model_autosave_on_exit: bool


    '''----------------------------------'''
    # Simulation
    ## Note these are multiplied together for a total count on a simulation run
    ## i.e. hmg = 100 with rbc = 10 produces 1000 games
    ## Batching should specifically be used when db persistence is enabled
    how_many_games: int
    runs_batch_count: int


    '''----------------------------------'''
    # Encoding
    state_encoding_dim_type: str # registerized in simulation/training/encoding/encoder_registry
    state_encoding_flattened: bool # interacts with dim type to provide a flat version of the selected type


    '''----------------------------------'''
    # Training
    online_training_enabled: bool
    offline_training_enabled: bool

    training_batch_size: int # How large do you want the training set to grow to until it starts training
    training_step_frequency: int # How often do you want to train i.e. every x steps
    

    '''----------------------------------'''    
    # Offline Agent / Reward
    offline_agent: str # registerized in players/computer_players/agent_registry
    offline_reward_type: str # registerized in simulation/rewards/reward_registry


    '''----------------------------------'''
    # Players
    player_types: list[Literal["human", "computer"]]

    ## If computer player
    ### Policy / Agent
    policy_type: list[Literal[
        "sequence_policy",
        "rl_dumb_policy",
        "q_learning_policy",
        "reverse_sequence_policy,"
        "planned_game_policy",
        "planned_game_policy2"
    ]] #registerized in players/computer_players/model_policy_registry
    agent_type: list[Literal[
        "rl_dumb_agent",
        "non_agent",
        "q_learning_agent"
    ]] # registerized in players/computer_players/agent_registry
    reward_type: list[Literal[
        "standard",
        "qlearn_tic_tac"
    ]] # registerized in simulation/rewards/reward_registry


    model_version: list[str] # Placeholder for - possibly when versions are dyamically built