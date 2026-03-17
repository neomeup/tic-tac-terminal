

class RunLogger:

    def __init__(self, passed_config):

        self.config = passed_config

        # Mongo
        if self.config.mongo_logging_enabled:
            from persistence.mongo.experience_repo import ExperienceRepository


            self.exp_repo = ExperienceRepository()

    def log_postgres(self, sim_uuid, payload):
        from persistence.postgres.postgres_connection import PostgresConnection

        from persistence.postgres.simulation_repo import SimulationRepository
        from persistence.postgres.game_moves_repo import GameRepository
        from persistence.postgres.players_repo import PlayersRepository

        from psycopg import Error as PostgresError

        postgres_conn = PostgresConnection()

        try:
            sim_repo = SimulationRepository(postgres_conn)
            player_repo = PlayersRepository(postgres_conn)
            game_repo = GameRepository(postgres_conn)

            sim_id = sim_repo.create_simulation_run(sim_uuid, **payload["simulation"])

            player_map = player_repo.get_or_create_players(payload["players"])

            game_repo.save_games_with_moves(sim_id, payload["games"], player_map)

            postgres_conn.commit()
        
        except (PostgresError, Exception) as e:
            postgres_conn.rollback()
            print("Rollback due to:\n", e)
            raise

        finally:
            postgres_conn.close()