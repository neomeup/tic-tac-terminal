def serialize_board(board):
    return [
        [
            None if cell is None else {
                "owner": cell.owner_id,
                "type": cell.piece_type
            }
            for cell in row
        ]
        for row in board
    ]