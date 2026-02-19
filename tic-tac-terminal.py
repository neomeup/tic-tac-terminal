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


import random
import curses
import textwrap
from config import GameConfig

config = GameConfig()


def draw_board(
        stdscr,
        config,
        player_1_pos: tuple[int, int],
        player_2_pos: tuple[int, int],
        board_lst: list[list[tuple[bool, bool, int]]],
        player_1_turn: bool
        ) -> tuple[bool, bool, bool]:
    
    x_character = config.x_char
    o_character = config.o_char
    empty_character = config.empty_char
    size = config.board_size

    stdscr.clear()
    
    ## Display start up information - dynamically sized
    height, width = stdscr.getmaxyx()


    # Verify that terminal size is large enough
    min_height = 15 + size
    min_width = 50


    if height < min_height or width < min_width:
        stdscr.clear()
        stdscr.addstr(0, 0, "Terminal too small!")
        stdscr.addstr(1, 0, f"Minimum size: {min_width}x{min_height}")
        stdscr.addstr(2, 0, f"Current size: {width}x{height}")
        stdscr.refresh()
        return False, False, False


    # Display Game info - auto scaled based on terminal size
    info_lines = [
        "This is a tic tac toe in CLI game that allows to take turns starting with 'O' or 'X' and replacing the empty character '-'",
        "Players can choose either X or O and one player will be randomly chosen to go first.",
        "The board will update after moves and declare a winner/loser or a draw once a win or draw condition is met."
    ]

    current_row = 0

    for line in info_lines:
        wrapped_text = textwrap.wrap(line, width - 5)
        for wrapped_line in wrapped_text:
            stdscr.addstr(current_row, 1, wrapped_line)
            current_row += 1
    

    # Display player turn
    if player_1_turn is True:
        active_player_message = "Player 1's turn!"
    elif player_1_turn is False:
        active_player_message = "Player 2's turn!"
    
    stdscr.addstr(current_row + 2, 1, f"{active_player_message}")
    
    # Display quit commands
    last_line = height
    last_column = width
    stdscr.addstr(last_line-1, 0, "'q' Quit player 1")
    stdscr.addstr(last_line-1, (last_column - 20), "'/' Quit player 2")

    # Board centering / positioning
    board_width = (size * 2) + 1
    
    col_start = (width - board_width) // 2  # Readability - col is read on the 2nd position [row, col] in addstr - inverse to mathematical graphs but matching addstr
    row_start = current_row + 5             # Readability - row is read on the 1st position [row, col] in addstr - inverse to mathematical graphs but matching addstr


    # Draw Game Board
    for row_index, row in enumerate(board_lst):
        for col_index, column in enumerate(row):

            # Logical board coordinates
            board_y = row_index
            board_x = col_index

            # Screen coordinates (2x spacing for vertical spacers)
            screen_y = row_start + board_y
            screen_x = col_start + (board_x * 2)

            # Determine which character to draw
            if not column[0] and not column[1]:
                char = empty_character
            elif column[0]:
                char = x_character
            else:
                char = o_character

            # Draw the cell (with highlight if active player selected)
            if (board_y, board_x) == player_1_pos and player_1_turn:
                stdscr.addstr(screen_y, screen_x, char, curses.color_pair(2))
            elif (board_y, board_x) == player_2_pos and not player_1_turn:
                stdscr.addstr(screen_y, screen_x, char, curses.color_pair(3))
            else:
                stdscr.addstr(screen_y, screen_x, char)

            # Draw vertical separator if not last column
            if col_index < size - 1:
                stdscr.addstr(screen_y, screen_x + 1, "|")


    # Determine game condition
    won_game, player_1_win, drawn_game = game_finished(config, board_lst)


    finish_condition = won_game, player_1_win, drawn_game

    stdscr.refresh()
    return finish_condition


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


def game_over_draw(stdscr, config, board_lst: list) -> None:
    size = config.board_size
    empty_character = config.empty_char
    x_character = config.x_char
    o_character = config.o_char

    stdscr.clear()
    
    
    # Verify that terminal size is large enough
    height, width = stdscr.getmaxyx()
    min_height = 10 + size
    min_width = 40

    if height < min_height or width < min_width:
        stdscr.clear()
        stdscr.addstr(0, 0, "Terminal too small!")
        stdscr.addstr(1, 0, f"Minimum size: {min_width}x{min_height}")
        stdscr.addstr(2, 0, f"Current size: {width}x{height}")
        stdscr.refresh()
        return
    

    stdscr.addstr(0, 0, "Game Finished!")
    stdscr.addstr(1, 0, "You have drawn the game!")

    board_width = (size * 2) - 1

    row_start = 5
    col_start = (width - board_width) // 2

    # Draw Game Board
    for row_index, row in enumerate(board_lst):
        for col_index, column in enumerate(row):

            # Logical board coordinates
            board_y = row_index
            board_x = col_index

            # Screen coordinates (2x spacing for vertical spacers)
            screen_y = row_start + board_y
            screen_x = col_start + (board_x * 2)

            # Determine which character to draw
            if not column[0] and not column[1]:
                char = empty_character
            elif column[0]:
                char = x_character
            else:
                char = o_character

            
            stdscr.addstr(screen_y, screen_x, char)

            # Draw vertical separator if not last column
            if col_index < size - 1:
                stdscr.addstr(screen_y, screen_x + 1, "|")


    # Display quit commands
    last_line = height
    last_column = width
    stdscr.addstr(last_line-1, 0, "'q' Quit player 1")
    stdscr.addstr(last_line-2, 0, "'n' Start a new game")
    stdscr.addstr(last_line-1, (last_column - 20), "'/' Quit player 2")


    stdscr.refresh()


def game_over_win(stdscr, config, player_1_win: bool, board_lst: list) -> None:
    size = config.board_size
    empty_character = config.empty_char
    x_character = config.x_char
    o_character = config.o_char

    stdscr.clear()
    
    
    # Verify that terminal size is large enough
    height, width = stdscr.getmaxyx()
    min_height = 10 + size
    min_width = 40

    if height < min_height or width < min_width:
        stdscr.clear()
        stdscr.addstr(0, 0, "Terminal too small!")
        stdscr.addstr(1, 0, f"Minimum size: {min_width}x{min_height}")
        stdscr.addstr(2, 0, f"Current size: {width}x{height}")
        stdscr.refresh()
        return
    
    # Display winning player message
    if player_1_win:
        won_game_message = "Good Job Player 1"
    elif not player_1_win:
        won_game_message = "Good Job Player 2 !"

    stdscr.addstr(0, 0, "Game Finished!")
    stdscr.addstr(1, 0, f"{won_game_message}")

    board_width = (size * 2) - 1

    row_start = 5
    col_start = (width - board_width) // 2

    # Draw Game Board
    for row_index, row in enumerate(board_lst):
        for col_index, column in enumerate(row):

            # Logical board coordinates
            board_y = row_index
            board_x = col_index

            # Screen coordinates (2x spacing for vertical spacers)
            screen_y = row_start + board_y
            screen_x = col_start + (board_x * 2)

            # Determine which character to draw
            if not column[0] and not column[1]:
                char = empty_character
            elif column[0]:
                char = x_character
            else:
                char = o_character

            
            stdscr.addstr(screen_y, screen_x, char)

            # Draw vertical separator if not last column
            if col_index < size - 1:
                stdscr.addstr(screen_y, screen_x + 1, "|")


    # Display quit commands
    last_line = height
    last_column = width
    stdscr.addstr(last_line-1, 0, "'q' Quit player 1")
    stdscr.addstr(last_line-2, 0, "'n' Start a new game")
    stdscr.addstr(last_line-1, (last_column - 20), "'/' Quit player 2")


    stdscr.refresh()


# Easy setup and tear down
curses.wrapper(main)