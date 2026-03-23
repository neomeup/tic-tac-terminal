'''
Registry mapping type name to policy classes.
'''

from players.computer_players.policies.sequence_policy import SequencePolicy
from players.computer_players.policies.rl_dumb_policy import RLDumbPolicy

model_policy_registry = {
    "sequence_policy": SequencePolicy,
    "rl_dumb_policy": RLDumbPolicy,
}