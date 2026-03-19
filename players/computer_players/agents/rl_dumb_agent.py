'''
Simple reinforcement learning agent for testing.

Holds policy and replay buffer for offline or online training.

Can be used as a template for more advanced learning and contains debugs for pipeline issues.
'''

import numpy as np

from players.computer_players.model_policy_registry import model_policy_registry
from simulation.training.buffer import ReplayBuffer

from players.computer_players.model_storage.infra.model_storage_factory import ModelStorageFactory
from players.computer_players.model_storage.infra.path_builder import ModelPathBuilder

class RLDumbAgent:

    def __init__(self, config, player_id, policy_name=None, capacity=10000):

        if policy_name is None:
            policy_name = "rl_dumb_policy"

        self.config = config
        self.player_id = player_id
        
        policy_class = model_policy_registry[policy_name]
        self.policy = policy_class()
        self.buffer = ReplayBuffer(capacity)

        self.storage = ModelStorageFactory.create(self.config)
        self.path_builder = ModelPathBuilder


    def _get_paths(self, checkpoint=None): # Placeholder checkpoint
        return self.path_builder.build_paths(config=self.config, player_id=self.player_id, checkpoint=checkpoint)
    
    def save(self, checkpoint=None):

        if self.storage is None:
            return
        
        paths = self._get_paths(checkpoint)
        
        model_bytes = self._serialize_model()
        metadata = self._build_metadata()

        self.storage.save_model(paths["model"], model_bytes)
        self.storage.save_metadata(paths["metadata"], metadata)

    def load(self, checkpoint=None):
        if self.storage is None:
            return
        
        paths = self._get_paths(checkpoint)

        model_bytes = self.storage.load_model(paths["model"])
        metadata = self.storage.load_metadata(paths["metadata"])

        self._serialize_model(model_bytes)
        self._load_metadata(metadata)

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