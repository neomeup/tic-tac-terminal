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


## Global Start Variables
x_char = "X"
o_char = "O"
empty_char = "-"
board_size = 4


def grab_globals(x_char,o_char,empty_char, board_size) -> tuple[str, str, str, int]:
    return x_char,o_char,empty_char, board_size


def board_lst_build(size: int) -> list :
    # initial board positions creation
    board_lst = []
    for x in range(size):
        board_lst.append(list(range(size)))

    # bool flags to notate if a square has been selected by a player or not
    p1_selected = False
    p2_selected = False

    # addition of selection flags to board positions
    for x in board_lst:
        for b in x:
            item = [p1_selected, p2_selected, b]
            x[b] = item
    return board_lst


def whose_turn() -> bool:
    turn_val = random.randint(0,1)
    if turn_val == 0:
        return True
    elif turn_val == 1:
        return False


def draw_board(
        stdscr,
        player_1_pos: tuple[int, int],
        player_2_pos: tuple[int, int],
        x_character: str,
        o_character: str,
        empty_character: str,
        board_lst: list[list[tuple[bool, bool, int]]],
        size: int,
        player_1_turn: bool
        ) -> tuple[bool, bool, bool]:
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
    won_game, player_1_win, drawn_game = game_finished(board_lst)


    finish_condition = won_game, player_1_win, drawn_game

    stdscr.refresh()
    return finish_condition


def game_finished(board_lst: list[list[tuple[bool, bool, int]]]) -> tuple[bool, bool, bool]:
    
    ##  All returns in following format -> won_game, player_1_win, drawn_game

    size = len(board_lst)
    win_length = 3 ## Should be move to globals eventually

    # Win helper
    # Helper function using win length to determine consecutive cells
    def consecutive_cells(cells_to_check: list, player_index: int) -> bool:
        cell_count = 0
        for cell in cells_to_check:
            if cell[player_index]:
                cell_count += 1
                if cell_count == win_length:
                    return True
            else:
                cell_count = 0
        return False
    
    # Stalemate helper
    # Helper function to return True if player could win the cells being checked
    def possible_line(cells_to_check, player_index):
        count = 0
        for cell in cells_to_check:
            if cell[player_index] or (not cell[0] and not cell[1]):
                count += 1
                if count >= win_length:
                    return True
            else:
                count = 0
        return False

    def build_rows(board_lst) -> list:
        row_lst = []
        for row in board_lst:
            row_lst.append(row)
        return row_lst


    def build_columns(board_lst) -> list:
        column_lst = []
        for col_index in range(size):
            column = [board_lst[row][col_index] for row in range(size)]
            column_lst.append(column)
        return column_lst
    

    def build_diagonals(board_lst) -> list:
        diagonal_lst = []
        # Moving row-wise
        for diag_index in range(size):
            diagonal_rows = []
            row = 0
            column = diag_index
            while row < size and column < size:
                diagonal_rows.append(board_lst[row][column])
                row += 1
                column += 1
            diagonal_lst.append(diagonal_rows)

        # Move column wise
        for diag_index in range(1, size): # Readability - possible to start at 1 due to initial diagonal already being checked in row-wise
            diagonal_columns = []
            row = diag_index
            column = 0
            while row < size and column < size:
                diagonal_columns.append(board_lst[row][column])
                row += 1
                column += 1
            diagonal_lst.append(diagonal_columns)
            
        # Move row wise
        for anti_diag_index in range(size - 1, 0, -1):
            anti_diagonal_rows = []
            row = 0
            column = anti_diag_index
            while row < size and column >= 0:
                anti_diagonal_rows.append(board_lst[row][column])
                row += 1
                column -= 1
            diagonal_lst.append(anti_diagonal_rows)
            
        # Move column wise
        for anti_diag_index in range(1, size):
            anti_diagonal_columns = []
            row = anti_diag_index
            column = size - 1
            while row < size and column >= 0:
                anti_diagonal_columns.append(board_lst[row][column])
                row += 1
                column -= 1
            diagonal_lst.append(anti_diagonal_columns)
        
        return diagonal_lst


    rows = build_rows(board_lst)
    columns = build_columns(board_lst)
    diagonals = build_diagonals(board_lst)


    # Win checking
    for i in rows:
        if consecutive_cells(i, 0) is True:
            return True, True, False
        if consecutive_cells(i, 1) is True:
            return True, False, False

    for i in columns:
        if consecutive_cells(i, 0) is True:
            return True, True, False
        if consecutive_cells(i, 1) is True:
            return True, False, False

    for i in diagonals:
        if consecutive_cells(i, 0) is True:
            return True, True, False
        if consecutive_cells(i, 1) is True:
            return True, False, False


    # Draw Checking
    for i in rows:
        if possible_line(i, 0) or possible_line(i, 1):
           return False, False, False
    
    for i in columns:
        if possible_line(i, 0) or possible_line(i, 1):
           return False, False, False

    for i in diagonals:
        if possible_line(i, 0) or possible_line(i, 1):
           return False, False, False       
    

    return False, False, True # Returns a game running state if no wins or draws are detected


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

    # Set Variables
    x_character,o_character,empty_character,size = grab_globals(x_char,o_char,empty_char, board_size)

    # Player position coordinates are in inverse graph notation [y axis,x axis] to match board list
    player_1_pos = [0,0]        # start position player 1
    player_2_pos = [0,(size-1)] # start position player 2
    
    player_1_turn = whose_turn()        # bool flag to mark whose turn it is - whose_turn() sets this randomly
    
    board_lst = board_lst_build(size)   # board initializer
    
    game_running = True
    build_new_game = True

    while True:
        stdscr.clear()

        # Initialize board setup for new games
        if build_new_game:
            board_lst = board_lst_build(size)
            player_1_pos = [0,0]        # start position player 1
            player_2_pos = [0,(size-1)] # start position player 2
            player_1_turn = whose_turn()
            build_new_game = False

        # Display the active game board
        if game_running:
            won_game, player_1_win, drawn_game = draw_board(stdscr, tuple(player_1_pos), tuple(player_2_pos), x_character, o_character, empty_character,board_lst, size, player_1_turn)
        
        if won_game is True:
            game_over_win(stdscr, player_1_win, size, board_lst, empty_character, x_character, o_character)
            game_running = False
        if drawn_game is True:
            game_over_draw(stdscr, size, board_lst, empty_character, x_character, o_character)
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


def game_over_draw(stdscr, size: int, board_lst: list, empty_character: str, x_character: str, o_character: str) -> None:
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


def game_over_win(stdscr, player_1_win: bool, size: int, board_lst: list, empty_character: str, x_character: str, o_character: str) -> None:
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



def board_list_select(player_1_turn: bool, player_coordinates: list, board_lst: list[list[tuple[bool, bool, int]]]) -> tuple[list, bool] :
    if player_1_turn is True:
        non_active_player = 1 # Player two is inactive
        active_player = 0 # Player one is active - corresponds to bool flags within board list
    elif player_1_turn is False:
        non_active_player = 0 # Player one is inactive
        active_player = 1 # Player two is active - corresponds to bool flags within board list

    changed_flag = False

    # Set Cell coordinates within board list
    y, x = player_coordinates
    working_cell = board_lst[y][x]

    if working_cell[non_active_player] is True:
        pass
    elif working_cell[active_player] is False:
        working_cell[active_player] = True
        changed_flag = True

    return board_lst, changed_flag



# Easy setup and tear down
curses.wrapper(main)