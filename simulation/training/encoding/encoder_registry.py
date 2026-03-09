from simulation.training.encoding.encoders.encode_vector import VectorEncode
from simulation.training.encoding.encoders.encode_tensor_players_only import TensorPlayersEncode

encoder_registry = {
    "vector": VectorEncode,
    "tensor_players": TensorPlayersEncode
}