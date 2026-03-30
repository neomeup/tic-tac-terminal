'''
Registry mapping type name to policy classes.
'''

from players.computer_players.policies.sequence_policy import SequencePolicy
from players.computer_players.policies.rl_dumb_policy import RLDumbPolicy
from players.computer_players.policies.q_learning_policy import QLearningPolicy
from players.computer_players.policies.reverse_sequence_policy import ReverseSequencePolicy
from players.computer_players.policies.planned_game_policy import PlannedGame
from players.computer_players.policies.planned_game_policy2 import PlannedGameTwo


model_policy_registry = {
    "sequence_policy": SequencePolicy,
    "rl_dumb_policy": RLDumbPolicy,
    "q_learning_policy": QLearningPolicy,
    "reverse_sequence_policy": ReverseSequencePolicy,
    "planned_game_policy": PlannedGame,
    "planned_game_policy2": PlannedGameTwo,

}