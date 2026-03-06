'''
For offline use with simulation result
'''

from simulation.training.experience import Experience

from simulation.training.encoders.action_encoder import encode_action
# Should be registerized as encode board currently builds 4 shapes of (3,3), (9,), (2,3,3) and (18,)
# Currently just returns the (9,)
from simulation.training.encoders.board_encoder import encode_board


class ExperienceDatasetBuilder:

    def __init__(self, simulation_result):
        self.result = simulation_result

    def build(self):
        experiences = []

        for run in self.result.runs:

            moves = run.moves

            for i in range(len(moves) - 1):

                current_move = moves[i]
                next_move = moves[i + 1]

                player_id = current_move["player_id"]

                state = encode_board(current_move["board_state"], player_id)
                next_state = encode_board(next_move["board_state"], player_id)

                board_size = len(current_move["board_state"])
                action = encode_action(current_move["action"], board_size)

                done = False
                reward = 0.0

                # Terminal reward logic 
                if i == len(moves) - 2:
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