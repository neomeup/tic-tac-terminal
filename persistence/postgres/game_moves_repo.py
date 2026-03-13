'''
Handles storage of data into games table and the moves table.
'''

from datetime import datetime
from .postgres_connection import PostgresConnection


class GameRepository:

    def __init__(self, connection: PostgresConnection | None = None):

        self.connection = connection or PostgresConnection()


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
        (simulation_run_id, game_id, player_id, player_id_in_game, turn_number, row, col, reward, board_state_json)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        total_moves = len(moves)
        now = datetime.utcnow()

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
                        move["board_state"]
                    )
                )

        self.connection.commit()

        return game_id