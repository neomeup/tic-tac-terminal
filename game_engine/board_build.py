## Build a grid that can be used interchangably with all game modes
def build_starting_board(size) -> list :
    # initial board positions creation
    board_lst = []
    for x in range(size):
        board_lst.append(list(range(size)))

    # Initial board ownership defined 
    for x in board_lst:
        for b in x:
            item = None
            x[b] = item
    return board_lst
