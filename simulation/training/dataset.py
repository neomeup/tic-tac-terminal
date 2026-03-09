'''
For offline use with simulation result
'''


from simulation.training.experience import Experience

from simulation.training.encoding.encoders.action_encoder import encode_action

from simulation.training.encoding.encoder_registry import encoder_registry


class ExperienceDatasetBuilder:

    def __init__(self, simulation_result, config):
        self.result = simulation_result
        self.config = config

        encoder_class = encoder_registry[self.config.state_encoding_dim_type]
        self.encoder = encoder_class(self.config)

    # Helper function for encoding
    def _encode_board(self, board_state, player_id):

        matrix = self.encoder.compute_encode(board_state, player_id)

        if self.config.state_encoding_flattened:
            return matrix.flatten()
        else: 
            return matrix

    def build(self):
        experiences = []

        for run in self.result.runs:

            moves = run.moves

            for i in range(len(moves) - 1):

                current_move = moves[i]
                next_move = moves[i + 1]

                player_id = current_move["player_id"]

                state = self._encode_board(current_move["board_state"], player_id)
                next_state = self._encode_board(next_move["board_state"], player_id)

                board_size = len(current_move["board_state"])
                action = encode_action(current_move["action"], board_size)

                done = False
                reward = 0.0

                # Terminal reward logic 
                if i == len(moves) - 2: # if last transition
                    done = True

                    if run.draw:
                        reward = 0.0
                    elif run.winner == current_move["player_id"]:
                        reward = 1.0
                    else:
                        reward = -1.0

                experiences.append(
                    Experience(
                        state=state,
                        action=action,
                        reward=reward,
                        next_state=next_state,
                        done=done,
                        player_id=current_move["player_id"]
                    )
                )

        return experiences