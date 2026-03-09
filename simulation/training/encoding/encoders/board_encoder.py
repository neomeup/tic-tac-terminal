import numpy as np


def encode_board(board_state, player_id) -> tuple[list, list, list, list]:
    '''
    Converts board to a numpy vectors with the following scheme for flat and 2d
    
    empty = 0
    own piece = 1
    enemy piece = -1

    and the following scheme for 3D (2,3,3)

    Player_id(tensor[0])
    own piece = 1
    empty or enemy = 0

    Returns a tuple of numpy arrays 

    Shapes:
    flattened vector = board size ^2
    2d = board size x board size
    
    Only players
    flattened tensor = player quantity * board size ^2
    3d = player quantity x board size x board size
    
    With empties as additional tensor
    flattened tensor = player quantity + 1 * board size ^2
    3d = player quantity + 1  x board size x board size

    '''
    size = len(board_state)

    player_quantity = len({cell["owner"] for row in board_state for cell in row if cell})

    vector = np.zeros((size, size), dtype=np.float32)

    tensor_players = np.zeros((player_quantity, size, size), dtype=np.float32)

    tensor_w_empty = np.zeros((player_quantity + 1, size, size), dtype=np.float32)

    for row in range(size):
        for col in range(size):

            cell = board_state[row][col]

            if cell is None:
                vector[row][col] = 0

            elif cell["owner"] == player_id:
                vector[row][col] = 1

            elif cell["owner"] != player_id: 
                vector[row][col] = -1
    

    for row in range(size):
        for col in range(size):
            for x in range(player_quantity):

                cell = board_state[row][col]

                if cell is None or cell["owner"] != x:
                    tensor_players[x][row][col] = 0
                
                elif cell["owner"] == x:
                    tensor_players[x][row][col] = 1
        

    for row in range(size):
        for col in range(size):
            for x in range(player_quantity + 1):

                cell = board_state[row][col]

                if cell is None and x == player_quantity:
                    tensor_w_empty[x][row][col] = 1

                elif cell is None:
                    tensor_w_empty[x][row][col] = 0

                elif cell["owner"] == x:
                    tensor_w_empty[x][row][col] = 1
                
                else: 
                    tensor_w_empty[x][row][col] = 0


    ## For all types but for debug continue with flat vector
    #return vector.flatten(), vector, tensor_players.flatten(), tensor_players, tensor_w_empty, tensor_w_empty.flatten()
    return vector.flatten()

'''
Debugging:

flat_board, non_flatten_board, tensor_players_flat, tensor_players, tensor_w_empty, tensor_w_empty_flat= (encode_board(([[{'owner': 1, 'type': 'standard_x-o'}, {'owner': 0, 'type': 'standard_x-o'}, {'owner': 1, 'type': 'standard_x-o'}], [{'owner': 0, 'type': 'standard_x-o'}, {'owner': 0, 'type': 'standard_x-o'}, {'owner': 0, 'type': 'standard_x-o'}], [{'owner': 1, 'type': 'standard_x-o'}, None, None]]),0))

print("Shape vector 2D:", non_flatten_board.shape)
print(non_flatten_board)

print("Shape flattened vector:", flat_board.shape)
print(flat_board)

print("Shape players only tensor 3D:", tensor_players.shape)
print(tensor_players)

print("Shape flattened players only tensor:", tensor_players_flat.shape)
print(tensor_players_flat)

print("Shape players and empties tensor:", tensor_w_empty.shape)
print(tensor_w_empty)

print("Shape flattened players and empties tensor:", tensor_w_empty_flat.shape)
print(tensor_w_empty_flat)

'''