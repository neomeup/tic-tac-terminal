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

import time
import random

from config import GameConfig
from renderers.cli_renderer import render_board, render_game_draw, render_game_won
from movement.human_players.human_movement import get_player_move
from movement.computer_players.computer_movement import get_computer_move
from game_types.used_rules import game_finished
from core.move import Move
from core.game_state import GameState
from core.run_context import GameRunContext
from core.serialization import serialize_board
from engine.board_build import build_starting_board
from engine.apply_move import apply_move

from simulation.engine import SimulationEngine

config = GameConfig()


def main(stdscr, config):
    def run_interactive_cli(stdscr, config):

        ## Start up curses for humans or observable computer play
        stdscr.clear()          # clear the screen
        curses.curs_set(0)      # prevents highlighted cursor from auto showing
        stdscr.nodelay(False)   # blocking input
        stdscr.keypad(True)     # enable arrow keys
        curses.noecho()

        # Color setup
        if curses.has_colors():                                             # check if the terminal supports color
            curses.start_color()                                            # enable color
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)      # white text on blue background
            stdscr.bkgd(' ', curses.color_pair(1))                          # fill entire screen with that color
            stdscr.clear()                                                  # clear screen to apply background
            curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)    # Player 1 highlight
            curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)     # Player 2 highlight

        size = config.board_size
        total_players = len(config.player_types)
        
        # Initial game state booleans
        game_running = True
        build_new_game = True

        # Initialize game count for computer vs computer rendered
        ## No game history is returned in rendered computer vs computer scenarios
        game_count = 1

        # Main logic loop for rendered games
        while True:
            stdscr.clear()

            # Initialize board setup for new games
            if build_new_game:
                board_lst = build_starting_board(config.board_size)
                player_1_pos = [0,0]        # start position player 1
                player_2_pos = [0,(size-1)] # start position player 2
                build_new_game = False
                if config.random_start:
                    current_player_index = random.randint(0, total_players - 1)
                else:
                    current_player_index = 0

            # Display the active game board if rendering
            if game_running:
                board_lst = render_board(stdscr, config, tuple(player_1_pos), tuple(player_2_pos), board_lst, current_player_index, game_count)
                won_game, winning_player, drawn_game = game_finished(config, board_lst)
            
            # Check game state for a finished game condition
            if won_game is True:
                render_game_won(stdscr, config, winning_player, board_lst, game_count)
                game_running = False
            elif drawn_game is True:
                render_game_draw(stdscr, config, board_lst, game_count)
                game_running = False
            
               

            # Determine player type

            current_player_type = config.player_types[current_player_index]

            # If computer type player, skip all curses and make move
            if current_player_type == "computer" and game_running:
                time.sleep(1)
                move = get_computer_move(current_player_index, board_lst, config)
                board_lst, changed_flag = apply_move(move, board_lst, config)
                if changed_flag is True:
                    current_player_index = (current_player_index + 1) % total_players

            # Game repeat/end control for computer vs computer rendered
            elif config.player_types[0] == "computer" and config.player_types[1] == "computer":
                if not game_running:
                    time.sleep(3.5)
                    if game_count == config.how_many_games:
                        break
                    else:
                        game_count += 1
                        game_running = True
                        build_new_game = True 
            # Grab keys if human player and game running
            else:
                ## Start grabbing inputs
                key = stdscr.getch()


                # Exits keys
                if key == ord("q"): #exit player 1
                    if current_player_index == 0 or not game_running:
                        break
                elif key == ord("/"): #exit player 2
                    if current_player_index == 1 or not game_running:
                        break
                
                # Terminal size refresher
                elif key == curses.KEY_RESIZE:
                    continue

                # New game key
                elif key == ord("n"):
                    if not game_running:
                        build_new_game = True
                        game_running = True

                ### Player movement tied to structure of board list - moves with the coordinates of board list
                elif key in [ord("w"), ord("a"), ord("s"), ord("d"), curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
                    if game_running:
                        if current_player_index == 0:
                            player_1_pos = get_player_move(key, current_player_index, player_1_pos, size, config)
                        elif current_player_index == 1:
                            player_2_pos = get_player_move(key, current_player_index, player_2_pos, size, config)

                ## Send action keys
                elif key == ord("e"): # Player 1 select
                    if current_player_index == 0:
                        move = Move(
                            player_id=current_player_index,
                            target_row=player_1_pos[0],
                            target_col=player_1_pos[1]
                        )
                        board_lst, changed_flag = apply_move(move, board_lst, config)
                        if changed_flag is True:
                            current_player_index = (current_player_index + 1) % total_players
                elif key in [curses.KEY_ENTER, 10, 13]: #Player 2 select
                    if current_player_index == 1:
                        move = Move(
                            player_id=current_player_index,
                            target_row=player_2_pos[0],
                            target_col=player_2_pos[1]
                        )
                        board_lst, changed_flag = apply_move(move, board_lst, config)
                        if changed_flag is True:
                            current_player_index = (current_player_index + 1) % total_players
                
                # Continue on non action key presses
                else:
                    continue
        

    if stdscr is not None:
        run_interactive_cli(stdscr,config)
    else:
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



# Easy setup and tear down
if config.render:
    if config.render_type == "cli":
        import curses
        curses.wrapper(lambda stdscr: main(stdscr, config))
else:
    main(None, config)