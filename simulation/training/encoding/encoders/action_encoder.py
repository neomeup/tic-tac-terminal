'''
Simple encoder to turn move objects into integers actions
'''

def encode_action(move, board_size, row=None, col=None):
    if row and col:
        action_encoded = (row * board_size) + col
        return action_encoded
    if move is None:
        return None
    
    action_encoded = (move["row"] * board_size) + move["col"]
    return action_encoded

def decode_action(encoded_value, board_size):
    row = encoded_value // board_size
    col = encoded_value % board_size
    return row, col