from configs.q_learning_training import get_config
from simulation.sim_engine import SimulationEngine

config = get_config()
find_first_only = False

def run_single_game(seed):

    # Control for seed finder
    config.random_seed = seed
    config.how_many_games = 1

    # Safe guarding data stream
    config.debug_prints_enabled = False
    config.model_storage_backend = None
    config.model_checkpoint_enabled = False
    config.model_autosave_on_exit = False
    config.postgres_logging_enabled = False
    config.mongo_logging_enabled = False
    config.render = False

    engine = SimulationEngine(config)
    result = engine.run()

    for game in result.runs:
        winner = game.winner


    if winner == 0:
        return 0
    elif winner == 1:
        return 1
    else:
        return -1

results = {
    "p0": [],
    "p1": [],
    "draw": []
}

for seed in range(1000):

    from players.computer_players.computer_player_runtime import _agents
    _agents.clear()

    result = run_single_game(seed)
    
    if result == 0:
        if find_first_only:
            if not results["p0"]:
                results["p0"].append(seed)
        else:
            results["p0"].append(seed)

    elif result == 1:
        if find_first_only:
            if not results["p1"]:
                results["p1"].append(seed)
        else:
            results["p1"].append(seed)

    else:
        if find_first_only:
            if not results["draw"]:
                results["draw"].append(seed)
        else:
            results["draw"].append(seed)

    # Early stop condition
    if find_first_only:
        if results["p0"] and results["p1"] and results["draw"]:
            break


print(results)