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
from engine import board_list_select, board_lst_build, whose_turn, game_finished
from renderer import draw_board, game_over_draw, game_over_win
from movement.player_movement import player_move
config = GameConfig()


def main(stdscr, config):
    def run_interactive(stdscr, config):

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
        
        # Initial game state booleans
        game_running = True
        build_new_game = True

        while True:
            stdscr.clear()

            # Initialize board setup for new games
            if build_new_game:
                board_lst = board_lst_build(config.board_size)
                player_1_pos = [0,0]        # start position player 1
                player_2_pos = [0,(size-1)] # start position player 2
                build_new_game = False
                if config.random_start:
                    player_1_turn = whose_turn()
                else:
                    player_1_turn = True

            # Display the active game board if rendering
            if game_running and config.render:
                won_game, player_1_win, drawn_game = draw_board(stdscr, config, tuple(player_1_pos), tuple(player_2_pos), board_lst, player_1_turn)
            elif game_running: # Return game state variables directly if not rendering
                won_game, player_1_win, drawn_game = game_finished(config, board_lst)
            
            if won_game is True:
                game_over_win(stdscr, config, player_1_win, board_lst)
                game_running = False
            if drawn_game is True:
                game_over_draw(stdscr, config, board_lst)
                game_running = False
            
            
            ## Start grabbing inputs
            key = stdscr.getch()


            # Exits keys
            if key == ord("q"): #exit player 1
                if player_1_turn or not game_running:
                    break
            elif key == ord("/"): #exit player 2
                if not player_1_turn or not game_running:
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
                    if player_1_turn:
                        player_1_pos = player_move(key, player_1_turn, player_1_pos, size)
                    elif not player_1_turn:
                        player_2_pos = player_move(key, player_1_turn, player_2_pos, size)

            ## Send action keys
            elif key == ord("e"): # Player 1 select
                if player_1_turn is True:
                    board_lst, changed_flag = board_list_select(player_1_turn,player_1_pos,board_lst)
                    if changed_flag is True:
                        player_1_turn = not player_1_turn
            elif key in [curses.KEY_ENTER, 10, 13]: #Player 2 select
                if player_1_turn is False:
                    board_lst, changed_flag = board_list_select(player_1_turn,player_2_pos,board_lst)
                    if changed_flag is True:
                        player_1_turn = not player_1_turn
            
            # Continue on non action key presses
            else:
                continue


    def run_headless():
        pass

    if stdscr is not None:
        run_interactive(stdscr,config)
    else:
        run_headless()



# Easy setup and tear down
if config.render:
    import curses
    curses.wrapper(lambda stdscr: main(stdscr, config))
else:
    main(None, config)