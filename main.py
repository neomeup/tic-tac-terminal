'''
This is a tic tac toe in CLI game that allows to take turns starting with "O" or "X" and replacing the empty character "-"
Players can choose either X or O and one player will be randomly chosen to go first.
The board will update after moves and declare a winner/loser or a draw once a win or draw condition is met. 
Puns: Tic-tac Terminated, tty1 - tic tac your terminal 
Example:
Day 26  Tic Tac Toe Board
X|O|-
-|X|-
O|-|X
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

    print(result)
    for game in result.runs:
        print("GameRunContext Object:", game)
        print("Game ID:", game.game_id)
        print("Winner:", game.winner)
        print("Moves:", len(game.moves))
        print("Final Board:", game.moves[len(game.moves)-1]["board_state"])
        print("--------")

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