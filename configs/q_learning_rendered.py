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
        random_start = False, # Start conditions for movement
        random_seed = 0, # Random Seed Config
        # for a single game, random seed 1 produces 0 winner, 37 for player 1 and 15 for draw

        #----------------------------------#        
        # Rendered runtime
        render = True,

        ## render_type is hardcoded for renderring in main.  If additional render types are built, this should be changed
        ## render_type is tied to movement for human players as well thus is changed this should change as well
        render_type = "cli", # Registerized in players/human_players/regsitry for selected type of movement for human players


        #----------------------------------#
        # Debugging
        debug_prints_enabled = False,
        debug_print_frequency_offline_batch = 1,
        debug_print_frequency_TransitionsSteps = 1,


        #----------------------------------#
        # Persistence
        mongo_logging_enabled = False,
        postgres_logging_enabled = False,

        model_storage_local_pre_base_path = "players/computer_players/model_storage/data",
        model_storage_backend = None,

        model_checkpoint_enabled = False,
        model_checkpoint_interval = 100, # In training steps 
        model_autosave_on_exit = False, # Should always be true to save the 'latest' 

        #restart from here

        #----------------------------------#
        # Simulation
        how_many_games = 1,


        #----------------------------------#
        # Encoding
        state_encoding_dim_type = "vector", # registerized in simulation/training/encoding/encoder_registry
        state_encoding_flattened = True, # interacts with dim type to provide a flat version of the selected type


        #----------------------------------#
        # Training
        online_training_enabled = False,
        offline_training_enabled = False,

        training_batch_size = 1, # How large do you want the training set to grow to until it starts training
        training_step_frequency = 1, # How often do you want to train i.e. every x steps
        

        #----------------------------------#    
        # Offline Agent / Reward
        offline_agent = "rl_dumb_agent", # registerized in players/computer_players/agent_registry
        offline_reward_type = "standard", # registerized in simulation/rewards/reward_registry


        #----------------------------------#
        # Players
        player_types = ["human", "computer"],

        ## If computer player
        ### Policy / Agent
        policy_type = ["q_learning_policy", "q_learning_policy"], #registerized in players/computer_players/model_policy_registry
        agent_type = ["q_learning_agent", "q_learning_agent"], # registerized in players/computer_players/agent_registry
        reward_type = ["qlearn_tic_tac", "qlearn_tic_tac"], # registerized in simulation/rewards/reward_registry


        model_version = ["v1", "v1"] # Placeholder for - possibly when versions are dyamically built
        )