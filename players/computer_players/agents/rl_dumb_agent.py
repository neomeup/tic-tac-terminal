'''
Simple reinforcement learning agent for testing.

Holds policy and replay buffer for offline or online training.

Can be used as a template for more advanced learning and contains debugs for pipeline issues.
'''

import numpy as np

from players.computer_players.model_policy_registry import model_policy_registry
from simulation.training.buffer import ReplayBuffer

class RLDumbAgent:

    def __init__(self, policy_name=None, capacity=10000):

        if policy_name is None:
            policy_name = "rl_dumb_policy"
        
        policy_class = model_policy_registry[policy_name]
        self.policy = policy_class()
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
            if getattr(exp, "player_id") is None:
                continue
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

        print(f"Stored experience for player {player_id} | reward={reward} | done={done}")
        print("Buffer size:", len(self.buffer))

    def train_step(self):
        # Debug for active pipes
        if len(self.buffer) < 1:
            return

        batch = self.buffer.sample(1)

        states = np.array([e["state"] for e in batch])
        rewards = np.array([e["reward"] for e in batch])
        dones = np.array([e["done"] for e in batch])
        action = np.array([e["action"] for e in batch])

        # Print for debug of encoding
        print("Train Step")
        print("Training batch:", batch)

        print("Training batch shape:", states.shape)
        print("Training action:", action)