from config import GameConfig

config = GameConfig


class RunLogger:

    def __init__(self, passed_config):

        self.config = passed_config

        # Mongo
        if config.mongo_logging_enabled:
            from persistence.mongo.experience_repo import ExperienceRepository


            self.exp_repo = ExperienceRepository()

        # Postgres
        if config.postgres_logging_enabled:
            from persistence.postgres.simulation_repo import SimulationRepository
            from persistence.postgres.game_moves_repo import GameRepository
            from persistence.postgres.players_repo import PlayersRepository


            self.sim_repo = SimulationRepository()
            self.player_repo = PlayersRepository()
            self.game_repo = GameRepository()