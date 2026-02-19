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


import curses
import textwrap
from config import GameConfig

config = GameConfig()


def main(stdscr):
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
            player_1_turn = whose_turn()
            build_new_game = False

        # Display the active game board
        if game_running:
            won_game, player_1_win, drawn_game = draw_board(stdscr, config, tuple(player_1_pos), tuple(player_2_pos), board_lst, player_1_turn)
        
        if won_game is True:
            game_over_win(stdscr, config, player_1_win, board_lst)
            game_running = False
        if drawn_game is True:
            game_over_draw(stdscr, config, board_lst)
            game_running = False
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

        ## Player 1 movement (wasd)
        elif key == ord("w"): #key up
            if player_1_turn is True: # Isolate movement by player turn for player 1
                player_1_pos[0] = max((0, player_1_pos[0] - 1))
        elif key == ord("s"): #key down
            if player_1_turn is True:
                player_1_pos[0] = min(((size-1), player_1_pos[0] + 1))
        elif key == ord("a"): #key left
            if player_1_turn is True:
                player_1_pos[1] = max((0, player_1_pos[1] - 1))
        elif key == ord("d"): #key right
            if player_1_turn is True:
                player_1_pos[1] = min(((size-1), player_1_pos[1] + 1))
    

        ## Player 2 movement (arrows)
        elif key == curses.KEY_UP: #key up
            if player_1_turn is False: # Isolate movement by player turn for player 2
                player_2_pos[0] = max((0, player_2_pos[0] - 1))
        elif key == curses.KEY_DOWN: #key down
            if player_1_turn is False:
                player_2_pos[0] = min(((size-1), player_2_pos[0] + 1))
        elif key == curses.KEY_LEFT: #key left
            if player_1_turn is False:
                player_2_pos[1] = max((0, player_2_pos[1] - 1))
        elif key == curses.KEY_RIGHT: #key right
            if player_1_turn is False:
                player_2_pos[1] = min(((size-1), player_2_pos[1] + 1))


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



# Easy setup and tear down
curses.wrapper(main)