'''
Entry point

Supports both CLI and headless modes. Handles:
- Game configuration
- Runtime selection (CLI vs headless simulation)
- Offline and online reinforcement learning
- Integration with agents, rules, and rewards
'''

from config import GameConfig
from simulation.sim_engine import SimulationEngine
from runtime.cli_runtime import CLIRuntime

from dotenv import load_dotenv

config = GameConfig()
load_dotenv()

def run_cli(config):
    import curses
    runtime = CLIRuntime(config)
    curses.wrapper(runtime.run)

def run_headless(config):
    engine = SimulationEngine(config)
    result = engine.run()

    # To view basic results in terminal output
    print(result)
    for game in result.runs:
        print("GameRunContext Object:", game)
        print("Game ID:", game.game_id)
        print("Winner:", game.winner)
        print("Moves:", len(game.moves))
        print("Final Board:", game.moves[len(game.moves)-1]["board_state"])
        print("--------")
    
    experiences = result.to_experiences(config)

    # For offline observe experiences
    #### To be changed/modified once trainer is introduced for offline so that you have a single agent persistance
    if config.offline_training_enabled:
        from players.computer_players.computer_player_runtime import offline_agent

        agent = offline_agent(config)
             
        print("----------")
        print("Offline")
        
        agent.observe(experiences)

        print("Total Experiences:", len(experiences))

    import uuid
    sim_id = str(uuid.uuid4())

    if config.mongo_logging_enabled:

        from persistence.mongo.document_builder import build_experience_document
        from persistence.run_logger import RunLogger
        
        documents = []
        for game_index, game in enumerate(result.runs):
            document = build_experience_document(game, sim_id, game_index, config)
            documents.append(document)

        try:
            logger = RunLogger(config)
            logger.log_mongo(documents)
        except Exception as e:
            print("-----mongo to storage-----")
            print(documents,"\n")
            print("\nMongo logging failed:", e)

    if config.postgres_logging_enabled:
        from persistence.postgres.table_builder import build_postgres_payloads
        from persistence.run_logger import RunLogger

        payload = build_postgres_payloads(result, config)

        try:
            logger = RunLogger(config)
            logger.log_postgres(sim_uuid=sim_id, payload=payload)
        except Exception as e:
            import pprint 
            print("-----Postgres connection/transaction failed-----")
            print("\nPayloads that would have been inserted:\n")
            pprint.pprint(payload)
            print("\nError details:\n", e)

    return result


# Easy setup and tear down
if config.render and config.render_type == "cli":
        try:
            run_cli(config)
        except KeyboardInterrupt:
            print("Exiting through KeyboardInterrupt by user")
            exit()
else:
    run_headless(config)