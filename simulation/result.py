'''
Combines multiple GameRunContexts into SimulationResults and builds experiences for training.
'''

from core.run_context import GameRunContext
from simulation.training.dataset import ExperienceDatasetBuilder


class SimulationResult:

    def __init__(self, runs: list[GameRunContext]):
        self.runs = runs


    # To connect to training for RL
    def to_experiences(self, config):
        builder = ExperienceDatasetBuilder(self, config)
        return builder.build()