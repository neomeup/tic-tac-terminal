
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
            if not getattr(exp, "player_id") == None:
                if hasattr(exp, "player_id"):
                    exp = {
                        "player_id": exp.player_id,
                        "reward": exp.reward,
                        "done": exp.done
                    }
                self.buffer.push(exp)

        # Debug buffer size
        print("Buffer size:", len(self.buffer))

        # Debug pipeline
        if len(self.buffer) >= 10:
            batch = self.buffer.sample(10)

            print("Sample batch:")
            for exp in batch:
                print(
                    "Player:", exp["player_id"],
                    "Reward:", exp["reward"],
                    "Done:", exp["done"]
                )
    
    def observe_transition(self, state, action, reward, next_state, done, player_id):
        
        if player_id is None:
            return 
        
        experience = {
            "state": state,
            "action": action,
            "reward": reward,
            "next_state": next_state,
            "done": done,
            "player_id": player_id
        }

        self.buffer.push(experience)

        print("Buffer size:", len(self.buffer))

    def train_step(self):
        # Placeholder for future batch training

        # Debug for fully active RL pipes
        print("Training step executed")
        pass


agent = RLDumbAgent()

def get_move(player_id, board, config, rng):
    return agent.select_action(player_id, board, config, rng)