'''
Handles retreiving of an existing player if it exists, otherwise creates one.
'''

from datetime import datetime
from .postgres_connection import PostgresConnection

class PlayersRepository:

    def __init__(self, connection: PostgresConnection | None = None):
        self.connection = connection or PostgresConnection()


    # Helper to be used with get_or_create_players()
    def get_or_create_player(
        self,
        account_user: str,
        player_type: str,
        agent_name: str | None = None,
        agent_version: str | None = None,
        policy_name: str | None = None,
        policy_version: str | None = None
        ) -> int:

        select_query = """
        SELECT id FROM players
        WHERE
            account_user = %s
            AND player_type = %s
            AND agent_name IS NOT DISTINCT FROM %s
            AND agent_version IS NOT DISTINCT FROM %s
            AND policy_name IS NOT DISTINCT FROM %s
            AND policy_version IS NOT DISTINCT FROM %s
        """

        insert_query = """
        INSERT INTO players
        (account_user, player_type, agent_name, agent_version, policy_name, policy_version, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """

        with self.connection.cursor() as cur:

            # Check if player already exists
            cur.execute(
                select_query,
                (
                    account_user,
                    player_type,
                    agent_name,
                    agent_version,
                    policy_name,
                    policy_version
                )
            )

            row = cur.fetchone()

            if row:
                return row[0]

            # Otherwise create new player
            cur.execute(
                insert_query,
                (
                    account_user,
                    player_type,
                    agent_name,
                    agent_version,
                    policy_name,
                    policy_version,
                    datetime.utcnow()
                )
            )

            player_id = cur.fetchone()[0]

        self.connection.commit()

        return player_id
    

    def get_or_create_players(self, players: list[dict]) -> dict[int, int]:

        player_id_map = {}
        for p in players:
            db_id = self.get_or_create_player(
                account_user=p["account_user"],
                player_type=p["player_type"],
                agent_name=p.get("agent_name"),
                agent_version=p.get("agent_version"),
                policy_name=p.get("policy_name"),
                policy_version=p.get("policy_version")
            )
            player_id_map[p["internal_id"]] = db_id
        return player_id_map