'''
Entry point

Supports both CLI and headless modes. Handles:
- Game configuration
- Runtime selection (CLI vs headless simulation)
- Offline and online reinforcement learning
- Integration with agents, rules, and rewards
'''

import time

import importlib
import importlib.util
import argparse
import os
import sys

from simulation.sim_engine import SimulationEngine
from runtime.cli_runtime import CLIRuntime

from dotenv import load_dotenv

def load_config(config_path: str):
    # File system path load
    if config_path.endswith(".py") or "/" in config_path:
        config_path = os.path.abspath(config_path)

        module_name = os.path.splitext(os.path.basename(config_path))[0]

        spec = importlib.util.spec_from_file_location(module_name, config_path)
        module = importlib.util.module_from_spec(spec)

        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        return module.get_config()

    # Module style load
    else:
        module = importlib.import_module(config_path)
        return module.get_config()

def run_cli(config):
    import curses
    runtime = CLIRuntime(config)
    curses.wrapper(runtime.run)

def run_headless(config):

    if config.runtime_sim_games:

        if config.mongo_logging_enabled:
            from persistence.mongo.document_builder import build_experience_document
            from persistence.run_logger import RunLogger

        if config.postgres_logging_enabled:
            from persistence.postgres.table_builder import build_postgres_payloads
            from persistence.run_logger import RunLogger

        import uuid
        sim_id = str(uuid.uuid4())

        results_list = []

        for batch in range(config.runs_batch_count):
            batch_id = batch + 1
            print(f"[Batch {batch_id}/{config.runs_batch_count}] Running simulation...")

            engine = SimulationEngine(config)
            result = engine.run()

            results_list.append(result)

            # To view basic results in terminal output
            if config.debug_prints_enabled:

                print("\n----- SimResults / Game Context -----")
                print(result)
                for index, game in enumerate(result.runs):
                    if index % config.debug_print_frequency_offline_batch == 0:
                        print("GameRunContext Object:", game)
                        print("Game ID:", game.game_id)
                        print("Winner:", game.winner)
                        print("Moves:", len(game.moves))
                        print("Final Board:", game.moves[len(game.moves)-1]["board_state"])
                        print("--------\n")

            if config.mongo_logging_enabled:

                if timing:
                    mongo_log_start_time = time.perf_counter()

                documents = []
                for game_index, game in enumerate(result.runs):
                    document = build_experience_document(game, sim_id, game_index, batch_id, config)
                    documents.append(document)

                try:
                    logger = RunLogger(config)
                    logger.log_mongo(documents)
                except Exception as e:
                    print("-----mongo to storage-----")
                    print(documents,"\n")
                    print("\nMongo logging failed:", e)

                if timing:
                    mongo_log_end_time = time.perf_counter()
                    total_elapsed_mongo_time = mongo_log_end_time - mongo_log_start_time
                    print(f"[Batch Logging Timing] Mongo storage completed in {total_elapsed_mongo_time:.4f}s")

            if config.postgres_logging_enabled:

                if timing:
                    postgres_log_start_time = time.perf_counter()

                payload = build_postgres_payloads(result, config)

                try:
                    logger = RunLogger(config)
                    logger.log_postgres(sim_uuid=sim_id, batch_id=batch_id, payload=payload)
                except Exception as e:
                    import pprint 
                    print("-----Postgres connection/transaction failed-----")
                    print("\nPayloads that would have been inserted:\n")
                    pprint.pprint(payload)
                    print("\nError details:\n", e)

                if timing:
                    postgres_log_end_time = time.perf_counter()
                    total_elapsed_postgres_time = postgres_log_end_time - postgres_log_start_time
                    print(f"[Batch Logging Timing] Postgres storage completed in {total_elapsed_postgres_time:.4f}s\n")

    # For offline observe experiences
    #### To be changed/modified once trainer is introduced for offline so that you have a single agent persistance
    if config.offline_training_enabled:

        from players.computer_players.computer_player_runtime import offline_agent

        if config.hybrid_runtime_offline_train:

            agent = offline_agent(config)

            for result_batch in results_list:

                experiences = result_batch.to_experiences(config)

                if config.debug_prints_enabled:
                    print("----- Offline -----")
                    print("Total Experiences:", len(experiences))
                
                agent.observe(experiences)

        if config.offline_train_only:

            agent = offline_agent(config)

            # load experiences from db
            # agent observe experiences
            # agent learn

            print("Offline only placeholder")

if __name__ == "__main__":
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Config module path (e.g. configs.full_persistence_3x3_sim)"
    )

    args = parser.parse_args()

    config = load_config(args.config)

    if config.render and config.render_type == "cli":
        try:
            run_cli(config)
        except KeyboardInterrupt:
            print("Exited by user")
    else:
        timing = config.timing

        if timing:
            start_total = time.perf_counter()

        run_headless(config)
        
        if timing:
            end_total = time.perf_counter()
            total_elapsed = end_total - start_total
            print(f"\n[Total Timing] Headless run completed in {total_elapsed:.2f}s")