
from movement.computer_players.policies.rl_dumb_policy import RLDumbPolicy
from simulation.training.buffer import ReplayBuffer

class RLDumbAgent:

    def __init__(self, capacity=10000):
        self.policy = RLDumbPolicy()
        self.buffer = ReplayBuffer(capacity)

    def select_action(self, player_id, board, config, rng):
        return self.policy.select_action(
            player_id,
            board,
            config,
            rng
        )

    def observe(self, experiences):
        """
        Accepts either:
        - single experience
        - list of experiences
        """

        if not isinstance(experiences, list):
            experiences = [experiences]

        for exp in experiences:
            self.buffer.push(exp)

        # Debug buffer size
        print("Buffer size:", len(self.buffer))

        # Debug pipeline
        if len(self.buffer) >= 4:
            batch = self.buffer.sample(4)

            print("Sample batch:")
            for e in batch:
                print(
                    "Player:", e.player_id,
                    "Reward:", e.reward,
                    "Done:", e.done
                )


    def train_step(self):
        # Placeholder for future batch training
        pass


agent = RLDumbAgent()

def get_move(player_id, board, config, rng):
    return agent.select_action(player_id, board, config, rng)