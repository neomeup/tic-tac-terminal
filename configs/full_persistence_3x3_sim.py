'''
Config for full persistence 
3x3 Board - Tic Tac Toe rule set
Simulation

'''

from configs.base_config import GameConfig

def get_config() -> GameConfig:
    return GameConfig(
        # Core game
        board_size = 3,
        x_char = "X",
        o_char = "O",
        empty_char = "-",
        win_length = 3, # Win length Tic-tac-toe/standard rule set

        ## - individually should be used as win/draw verification
        ## - logic ties to apply_move which checks for a valid move thus this should be changed if play rules change i.e. captures
        rule_set = "standard", # registerized in game_types/rules_registry
        piece_type = "standard_x-o", # Could be registerized if you want multiple piece types - would be tied to rules


        #----------------------------------#
        # Random runtime 
        random_start = True, # Start conditions for movement
        random_seed = None, # Random Seed Config


        #----------------------------------#        
        # Rendered runtime
        render = False,

        ## render_type is hardcoded for renderring in main.  If additional render types are built, this should be changed
        ## render_type is tied to movement for human players as well thus is changed this should change as well
        render_type = "cli", # Registerized in players/human_players/regsitry for selected type of movement for human players


        #----------------------------------#
        # Debugging
        debug_prints_enabled = True,
        debug_print_frequency_offline_batch = 5,
        debug_print_frequency_TransitionsSteps = 5,

        # Timing
        timing = False,

        
        #----------------------------------#
        # Persistence
        mongo_logging_enabled = True,
        postgres_logging_enabled = True,

        model_storage_local_pre_base_path = "players/computer_players/model_storage/data",
        model_storage_backend = None,

        model_checkpoint_enabled = True,
        model_checkpoint_interval = 5, # In training steps 
        model_autosave_on_exit = True,


        #----------------------------------#
        # Simulation
        ## Note these are multiplied together for a total count on a simulation run
        ## i.e. hmg = 100 with rbc = 10 produces 1000 games
        ## Batching should specifically be used when db persistence is enabled
        how_many_games = 1,
        runs_batch_count = 1,


        #----------------------------------#
        # Encoding
        state_encoding_dim_type = "tensor_with_empty", # registerized in simulation/training/encoding/encoder_registry
        state_encoding_flattened = True, # interacts with dim type to provide a flat version of the selected type


        #----------------------------------#
        # Training
        online_training_enabled = True,
        offline_training_enabled = True,

        training_batch_size = 5, # How large do you want the training set to grow to until it starts training
        training_step_frequency = 5, # How often do you want to train i.e. every x steps
        

        #----------------------------------#    
        # Offline Agent / Reward
        offline_agent = "rl_dumb_agent", # registerized in players/computer_players/agent_registry
        offline_reward_type = "standard", # registerized in simulation/rewards/reward_registry


        #----------------------------------#
        # Players
        player_types = ["computer", "computer"],

        ## If computer player
        ### Policy / Agent
        policy_type = ["rl_dumb_policy", "sequence_policy"], #registerized in players/computer_players/model_policy_registry
        agent_type = ["rl_dumb_agent", "non_agent"], # registerized in players/computer_players/agent_registry
        reward_type = ["standard", "standard"], # registerized in simulation/rewards/reward_registry

        model_version = ["v1", "v1"], # Placeholder for - possibly when versions are dyamically built
        )