'''
This is a tic tac toe in CLI game that allows to take turns starting with "O" or "X" and replacing the empty character "-"
The board will update after moves and declare a winner/loser or a draw once a win or draw condition is met.

You can play human vs human, human vs computer or computer vs computer.

For computer vs computer play, you have the option to run a headless simulation.

All control variables are set through config and you can find the different options/names for #registerized components in
their corresponding registries.

Have fun and happy learning!

Puns: Tic-tac Terminated, tty1 - tic tac your terminal
'''

from config import GameConfig
from simulation.engine import SimulationEngine
from runtime.cli_runtime import CLIRuntime

config = GameConfig()

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
    
    experiences = result.to_experiences()

    # For offline observe experiences
    #### To be changed/modified once trainer is introduced for offline so that you have a single agent persistance
    if config.offline_training_enabled:
        from movement.computer_players.computer_movement import offline_agent

        agent = offline_agent(config)
             
        print("----------")
        print("Offline")
        
        agent.observe(experiences)

        print("Total Experiences:", len(experiences))

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