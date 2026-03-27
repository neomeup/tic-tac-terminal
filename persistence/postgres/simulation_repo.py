'''
Handles storage of data into simulation runs table
'''

from datetime import datetime
from psycopg.types.json import Json


class SimulationRepository:

    def __init__(self, conn):

        self.connection = conn

    def create_simulation_run(self, sim_uuid: str, rule_set: str, encoder: str, reward_system_player_1: str, reward_system_player_2: str, num_games: int, config_json: dict) -> int:

        query = """
        INSERT INTO simulation_runs
        (sim_uuid, rule_set, encoder, reward_system_player_1, reward_system_player_2, num_games, created_at, config_json)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """

        with self.connection.cursor() as cur:

            cur.execute(
                query,
                (
                    sim_uuid,
                    rule_set,
                    encoder,
                    reward_system_player_1,
                    reward_system_player_2,
                    num_games,
                    datetime.utcnow(),
                    Json(config_json)
                )
            )

            simulation_id = cur.fetchone()[0]

        return simulation_id