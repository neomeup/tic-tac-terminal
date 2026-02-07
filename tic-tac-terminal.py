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
board_size = 3


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

    
    #Handling of spacer character |
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
            


    
    won_game = False
    player_1_win = False
    drawn_game = False

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
    
    player_1_turn = whose_turn()        # bool flag to mark whose turn it is
    
    board_lst = board_lst_build(size)   # board initializer
    
    while True:
        stdscr.clear()
        draw_board(stdscr, tuple(player_1_pos), tuple(player_2_pos), x_character, o_character, empty_character,board_lst, size, player_1_turn)
        key = stdscr.getch()


        # Exits keys
        if key == ord("q"): #exit player 1
            break
        elif key == ord("/"): #exit player 2
            break
        

        ### Player movement tied to structure of board list - moves with the coordinates of board list

        if player_1_turn is True: # Isolate movement by player turn for player 1
            ## Player 1 movement (wasd)
            if key == ord("w"): #key up
                player_1_pos[0] = max((0, player_1_pos[0] - 1))
            elif key == ord("s"): #key down
                player_1_pos[0] = min(((size-1), player_1_pos[0] + 1))
            elif key == ord("a"): #key left
                player_1_pos[1] = max((0, player_1_pos[1] - 1))
            elif key == ord("d"): #key right
                player_1_pos[1] = min(((size-1), player_1_pos[1] + 1))
        
        if player_1_turn is False: # Isolate movement by player turn for player 2
            ## Player 2 movement (arrows)
            if key == curses.KEY_UP: #key up
                player_2_pos[0] = max((0, player_2_pos[0] - 1))
            elif key == curses.KEY_DOWN: #key down
                player_2_pos[0] = min(((size-1), player_2_pos[0] + 1))
            elif key == curses.KEY_LEFT: #key left
                player_2_pos[1] = max((0, player_2_pos[1] - 1))
            elif key == curses.KEY_RIGHT: #key right
                player_2_pos[1] = min(((size-1), player_2_pos[1] + 1))


        ## Send action keys
        elif key == ord("e"): # Player 1 select
            board_lst = board_list_select(player_1_turn,player_1_pos,board_lst)
            player_1_turn = False
        elif key in [curses.KEY_ENTER, 10, 13]: #Player 2 select
            board_lst = board_list_select(player_1_turn,player_2_pos,board_lst)
            player_1_turn = True

        else:
            continue


def board_list_select(player_1_turn: bool, player_coordinates: list, board_lst: list[list[tuple[bool, bool, int]]]) -> list :
    if player_1_turn is True:
        non_active_player = 1 # Player two is inactive
        active_player = 0 # Player one is active - corresponds to bool flags within board list
    elif player_1_turn is False:
        non_active_player = 0 # Player one is inactive
        active_player = 1 # Player two is active - corresponds to bool flags within board list

    for row in board_lst:
        if row == board_lst[player_coordinates[0]]: # Identify selected row
            for column in row:
                if column == row[player_coordinates[1]]: # Identify selected column
                    if column[non_active_player] is True: # Prevent double true selections
                        pass  ## Possible addition of a separate flag to denote errors/impossible selection
                    else:
                        column[active_player] = True # Change selected square to show as marked

    return board_lst



# This handles setup and teardown safely
curses.wrapper(main)