from simulation.training.experience import Experience


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

                state = current_move["board_state"]
                action = current_move["action"]
                next_state = next_move["board_state"]

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