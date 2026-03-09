'''
Holds simulation results and provides utility methods.
'''

from core.run_context import GameRunContext
from simulation.training.dataset import ExperienceDatasetBuilder


class SimulationResult:

    def __init__(self, runs: list[GameRunContext]):
        self.runs = runs


    # Example helpers using sim result class
    def winners(self):
        return [r.winner for r in self.runs]

    def win_rate(self, player_id):
        total_games = len(self.runs)
        wins = sum(1 for r in self.runs if r.winner == player_id)
        return wins / total_games if total_games > 0 else 0

    def average_moves(self):
        if not self.runs:
            return 0

        return sum(len(r.moves) for r in self.runs) / len(self.runs)


    # Data flattening of moves
    def to_training_dataset(self):
        dataset = []

        for run in self.runs:
            for move in run.moves:
                dataset.append(move)

        return dataset


    # For db storage and Dashboard integration, return non full logs
    def to_dict(self):
        return {
            "games": [
                {
                    "game_id": r.game_id,
                    "winner": r.winner,
                    "moves": len(r.moves),
                }
                for r in self.runs
            ]
        }
    
    # To connect to training for RL
    def to_experiences(self, config):
        builder = ExperienceDatasetBuilder(self, config)
        return builder.build()