'''
renderer should handle only the curses rendering of game screen, win screen, and draw screen.
-- all future rendered screens should be located here
'''

import curses
import textwrap


## Render the board during gameplay
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

            # Draw the cell (with highlight if active player selected) - if computer player, no highlight
            if player_1_turn:
                current_player_index = 0
            else:
                current_player_index = 1
            current_player_type = config.player_types[current_player_index]

            if current_player_type == "computer":
                stdscr.addstr(screen_y, screen_x, char)
            elif (board_y, board_x) == player_1_pos and player_1_turn:
                stdscr.addstr(screen_y, screen_x, char, curses.color_pair(2))
            elif (board_y, board_x) == player_2_pos and not player_1_turn:
                stdscr.addstr(screen_y, screen_x, char, curses.color_pair(3))
            else:
                stdscr.addstr(screen_y, screen_x, char)

            # Draw vertical separator if not last column
            if col_index < size - 1:
                stdscr.addstr(screen_y, screen_x + 1, "|")

    stdscr.refresh()
    return board_lst


## Render the game won screen
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


## Render the drawn game screen
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