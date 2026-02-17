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
        player_1: tuple[int, int],
        player_2: tuple[int, int],
        x_character: str,
        o_character: str,
        empty_character: str,
        board_lst: list[list[tuple[bool, bool, int]]],
        size: int,
        player_1_turn: bool
        ) -> tuple[bool, bool, bool]:
    stdscr.clear()
    stdscr.addstr(0, 10, "This is a tic tac toe in CLI game that allows to take turns starting with 'O' or 'X' and replacing the empty character '-'")
    stdscr.addstr(1, 10, "Players can choose either X or O and one player will be randomly chosen to go first.")
    stdscr.addstr(2, 10, "The board will update after moves and declare a winner/loser or a draw once a win or draw condition is met.")
    

    # Display player turn
    if player_1_turn is True:
        active_player_message = "Player 1's turn!"
    elif player_1_turn is False:
        active_player_message = "Player 2's turn!"
    
    stdscr.addstr(3, 10, f"{active_player_message}")
    
    
    
    
    #               # Readability - Board_lst is built using mathematical notation with typical [x,y] coordinates
    col_start = 30  # Readability - col is read on the 2nd position [row, col] in addstr - inverse to mathematical graphs but matching addstr
    row_start = 5   # Readability - row is read on the 1st position [row, col] in addstr - inverse to mathematical graphs but matching addstr

    
    #Handling of vertical spacing character |
    space_char_lst = []
    for x in range((size*2)-1):
        if x % 2 == 1:
            space_char_lst.append(x)
    
    row_index = 0
    ## Some sort of handling of if a player tries to overwrite an already true location
    for row in board_lst:
        col_index = 0
        for column in row:
            if column[0] is False and column[1] is False:
                stdscr.addstr((row_start+row_index), (col_start+col_index), empty_character)
                for x in space_char_lst:
                    stdscr.addstr((row_start+row_index), (col_start+x), "|")
            elif column[0] is True:
                stdscr.addstr((row_start+row_index), (col_start+col_index), x_character)
                for x in space_char_lst:
                    stdscr.addstr((row_start+row_index), (col_start+x), "|")
            elif column[1] is True:
                stdscr.addstr((row_start+row_index), (col_start+col_index), o_character)
                for x in space_char_lst:
                    stdscr.addstr((row_start+row_index), (col_start+x), "|")                             
            col_index += 2
        row_index += 1
            


    won_game, player_1_win, drawn_game = game_finished(board_lst)

    finish_condition = won_game, player_1_win, drawn_game

    stdscr.refresh()
    return finish_condition


def game_finished(board_lst: list[list[tuple[bool, bool, int]]]) -> tuple[bool, bool, bool]:
    
    ##  All returns in following format -> won_game, player_1_win, drawn_game

    size = len(board_lst)
    win_length = 3 ## Should be move to globals eventually


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
    

    ## All win logic is generally separate into two parts
    #  - isolate line type 
    #  - pass line type to consec_cells as cells to check for each player

    # Row wins
    for row in board_lst:                       # Build rows for consec_cells()
        if consecutive_cells(row, 0) is True:   # Check player 1
            return True, True, False
        if consecutive_cells(row, 1) is True:   # Check player 2
            return True, False, False    
        

    # Column wins
    for col_index in range(size):
        column = [board_lst[row][col_index] for row in range(size)]
        if consecutive_cells(column, 0) is True:
            return True, True, False
        if consecutive_cells(column, 1) is True:
            return True, False, False



    ## Forward diagonals (all possible - needed for larger boards with different win lengths)
    # Moving row-wise
    for diag_index in range(size):
        diagonal_forward = []
        row = 0
        column = diag_index
        while row < size and column < size:
            diagonal_forward.append(board_lst[row][column])
            row += 1
            column += 1
        if consecutive_cells(diagonal_forward, 0) is True:
            return True, True, False
        if consecutive_cells(diagonal_forward, 1) is True:
            return True, False, False

    # Move column wise
    for diag_index in range(1, size): # Readability - possible to start at 1 due to initial diagonal already being checked in row-wise
        diagonal_backwards = []
        row = diag_index
        column = 0
        while row < size and column < size:
            diagonal_backwards.append(board_lst[row][column])
            row += 1
            column += 1
        if consecutive_cells(diagonal_backwards, 0) is True:
            return True, True, False
        if consecutive_cells(diagonal_backwards, 1) is True:
            return True, False, False
        

    ## Backwards diagonals
    # Move row wise
    for anti_diag_index in range(size - 1, 0, -1):
        anti_diagonal_rows = []
        row = 0
        column = anti_diag_index
        while row < size and column >= 0:
            anti_diagonal_rows.append(board_lst[row][column])
            row += 1
            column -= 1
        if consecutive_cells(anti_diagonal_rows, 0) is True:
            return True, True, False
        if consecutive_cells(anti_diagonal_rows, 1) is True:
            return True, False, False
        
    # Move column wise
    for anti_diag_index in range(1, size):
        anti_diagonal_columns = []
        row = anti_diag_index
        column = size - 1
        while row < size and column >= 0:
            anti_diagonal_columns.append(board_lst[row][column])
            row += 1
            column -= 1
        if consecutive_cells(anti_diagonal_columns, 0) is True:
            return True, True, False
        if consecutive_cells(anti_diagonal_columns, 1) is True:
            return True, False, False




    return False, False, False


def main(stdscr):
    stdscr.clear()          # clear the screen
    curses.curs_set(0)      # prevents highlighted cursor from auto showing
    stdscr.nodelay(False)   # blocking input
    stdscr.keypad(True)     # enable arrow keys
    curses.noecho()

    # Color setup
    if curses.has_colors():                                         # check if the terminal supports color
        curses.start_color()                                        # enable color
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)  # white text on blue background
        stdscr.bkgd(' ', curses.color_pair(1))                      # fill entire screen with that color
        stdscr.clear()                                              # clear screen to apply background

    # Set Variables
    x_character,o_character,empty_character,size = grab_globals(x_char,o_char,empty_char, board_size)

    # Player position coordinates are in inverse graph notation [y axis,x axis] to match board list
    player_1_pos = [0,0]        # start position player 1
    player_2_pos = [0,(size-1)] # start position player 2
    
    player_1_turn = whose_turn()        # bool flag to mark whose turn it is - whose_turn() sets this randomly
    
    board_lst = board_lst_build(size)   # board initializer
    
    while True:
        stdscr.clear()
        won_game, player_1_win, drawn_game = draw_board(stdscr, tuple(player_1_pos), tuple(player_2_pos), x_character, o_character, empty_character,board_lst, size, player_1_turn)
        if won_game is True:
            if player_1_win is True:
                break
            elif player_1_win is False:
                break
        if drawn_game is True:
            break
        key = stdscr.getch()


        # Exits keys
        if key == ord("q"): #exit player 1
            break
        elif key == ord("/"): #exit player 2
            break
        

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



# This handles setup and teardown safely
curses.wrapper(main)