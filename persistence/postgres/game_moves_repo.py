'''
Handles storage of data into games table and the moves table.
'''

from datetime import datetime
from psycopg.types.json import Json


class GameRepository:

    def __init__(self, conn):

        self.connection = conn


    def save_game_with_moves(
        self,
        simulation_run_id: int,
        player_one_id: int,
        player_two_id: int,
        winner_player_id: int | None,
        winner_in_game_id: int | None,
        is_draw: bool,
        moves: list[dict]
        ) -> int:

        game_query = """
        INSERT INTO games
        (
            simulation_run_id,
            player_one_id,
            player_two_id,
            winner_player_id,
            winner_in_game_id,
            is_draw,
            total_moves,
            created_at
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
        """

        move_query = """
        INSERT INTO moves
        (simulation_run_id, game_id, player_id, player_id_in_game, turn_number, row_index, col_index, reward, board_state_json)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        total_moves = len(moves)
        now = datetime.utcnow()

        # Debug forced break to test rollback
        #player_one_id = 9999999999999

        with self.connection.cursor() as cur:

            # Insert game
            cur.execute(
                game_query,
                (
                    simulation_run_id,
                    player_one_id,
                    player_two_id,
                    winner_player_id,
                    winner_in_game_id,
                    is_draw,
                    total_moves,
                    now,
                )
            )

            game_id = cur.fetchone()[0]

            # Insert moves
            for move in moves:

                cur.execute(
                    move_query,
                    (
                        simulation_run_id,
                        game_id,
                        move["player_id"],
                        move["player_id_in_game"],
                        move["turn"],
                        move["row"],
                        move["col"],
                        move["reward"],
                        Json(move["board_state"])
                    )
                )

        return game_id
    
    def save_games_with_moves(
        self,
        simulation_run_id: int,
        games: list[dict],
        player_map: dict[int, int]
        ) -> None:

        player_one_id = player_map[0]
        player_two_id = player_map[1]

        for game in games:

            winner_in_game_id = game["winner"]
            is_draw = game["draw"]

            if is_draw or winner_in_game_id is None:
                winner_player_id = None
            else:
                winner_player_id = player_map[winner_in_game_id]

            moves = []

            for move in game["moves"]:

                db_player_id = player_map.get(move["player_id_in_game"])

                moves.append({
                    "player_id": db_player_id,
                    "player_id_in_game": move["player_id_in_game"],
                    "turn": move["turn"],
                    "row": move["row"],
                    "col": move["col"],
                    "reward": move["reward"],
                    "board_state": move["board_state"],
                })

            self.save_game_with_moves(
                simulation_run_id=simulation_run_id,
                player_one_id=player_one_id,
                player_two_id=player_two_id,
                winner_player_id=winner_player_id,
                winner_in_game_id=winner_in_game_id,
                is_draw=is_draw,
                moves=moves
            )