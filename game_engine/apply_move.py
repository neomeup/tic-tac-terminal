from core.piece import Piece
from core.move import Move

def apply_move(move: Move, board_lst: list[list], config) -> tuple[list, bool]:
    row = move.target_row
    col = move.target_col

    if board_lst[row][col] is not None:
        return board_lst, False  # changed flag is false due to invalid

    board_lst[row][col] = Piece(
        owner_id=move.player_id,
        piece_type=config.piece_type
    )

    return board_lst, True