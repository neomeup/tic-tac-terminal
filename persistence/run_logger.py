

class RunLogger:

    def __init__(self, passed_config):

        self.config = passed_config

    def log_mongo(self, documents):
            from persistence.mongo.mongo_connection import MongoConnection


            from persistence.mongo.experience_repo import ExperienceRepository

            mongo_conn = MongoConnection()

            exp_repo = ExperienceRepository(mongo_conn)

            exp_repo.insert_many(documents)


    def log_postgres(self, sim_uuid, batch_id, payload):
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

            sim_id = sim_repo.create_simulation_run(sim_uuid, batch_id, **payload["simulation"])

            player_map = player_repo.get_or_create_players(payload["players"])

            game_repo.save_games_with_moves(sim_id, batch_id, payload["games"], player_map)

            postgres_conn.commit()
        
        except (PostgresError, Exception) as e:
            postgres_conn.rollback()
            print("Rollback due to:\n", e)
            raise

        finally:
            postgres_conn.close()