'''
Function to create starting board for Tic-Tac-Toe style games (squares with no starting pieces)

Supports variable board sizes through config
'''

def build_starting_board(size) -> list :
    board_lst = []
    for x in range(size):
        board_lst.append(list(range(size)))

    for x in board_lst:
        for b in x:
            item = None
            x[b] = item
    return board_lst
