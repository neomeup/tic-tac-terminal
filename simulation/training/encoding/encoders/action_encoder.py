'''
Simple encoder to turn move objects into integers actions
'''

def encode_action(move, board_size):
    if move is None:
        return None
    
    action_encoded = (move["row"] * board_size) + move["col"]
    return action_encoded