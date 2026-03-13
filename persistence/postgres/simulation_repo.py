'''
Handles storage of data into simulation runs table
'''

from datetime import datetime
from .postgres_connection import PostgresConnection


class SimulationRepository:

    def __init__(self, connection: PostgresConnection | None = None):

        self.connection = connection or PostgresConnection()

    def create_simulation_run(self, rule_set: str, encoder: str, reward_system: str, num_games: int, config_json: dict) -> int:

        query = """
        INSERT INTO simulation_runs
        (rule_set, encoder, reward_system, num_games, created_at, config_json)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
        """

        with self.connection.cursor() as cur:

            cur.execute(
                query,
                (
                    rule_set,
                    encoder,
                    reward_system,
                    num_games,
                    datetime.utcnow(),
                    config_json
                )
            )

            simulation_id = cur.fetchone()[0]

        self.connection.commit()

        return simulation_id