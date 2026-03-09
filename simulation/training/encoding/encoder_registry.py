'''
Registry mapping of encoder names to encoder classes.

Supports dynamic selection of state encoding in simulations and RL.
'''

from simulation.training.encoding.encoders.encode_vector import VectorEncode
from simulation.training.encoding.encoders.encode_tensor_players_only import TensorPlayersEncode
from simulation.training.encoding.encoders.encode_tensor_w_empty import TensorPlayersWithEmptyEncode

encoder_registry = {
    "vector": VectorEncode,
    "tensor_players": TensorPlayersEncode,
    "tensor_with_empty": TensorPlayersWithEmptyEncode
}