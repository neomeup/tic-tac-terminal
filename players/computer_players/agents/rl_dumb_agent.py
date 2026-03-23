'''
Simple reinforcement learning agent for testing.

Holds policy and replay buffer for offline or online training.

Can be used as a template for more advanced learning and contains debugs for pipeline issues.
'''

import numpy as np

import io
import torch
from datetime import datetime


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

        self.training_step = 0 # Initialization
        self.training_batch_size = config.training_batch_size

        self.storage = ModelStorageFactory.create(self.config)
        self.path_builder = ModelPathBuilder() #static method so instantiation not neccessary but possible necessity in future

        # Debug counter for transitions and train steps
        self.debug_TransitionsSteps_count = 0 

    def _get_paths(self, checkpoint=None): # Placeholder checkpoint
        return self.path_builder.build_paths(config=self.config, player_id=self.player_id, checkpoint=checkpoint)

    def _serialize_model(self):
        buffer = io.BytesIO()

        state_dict = None
        if hasattr(self.policy, "state_dict"):
            state_dict = self.policy.state_dict()

        torch.save({
            "policy_state": state_dict,
        }, buffer)

        return buffer.getvalue()

    def _build_metadata(self, checkpoint=None):

        checkpoint = checkpoint if checkpoint is not None else "latest"
        
        return {
            "board_size": self.config.board_size,
            "rule_set": self.config.rule_set,

            "win_length": self.config.win_length,
            "piece_type": self.config.piece_type,

            "agent": self.config.agent_type[self.player_id],
            "agent_version": self.config.model_version[self.player_id],

            "policy": self.config.policy_type[self.player_id],
            "policy_version": "v1", # Placeholder

            "checkpoint": checkpoint,

            "player_id": self.player_id,

            "created_at": datetime.utcnow().isoformat(),

            # Placeholder training info
            "buffer_size": len(self.buffer),
            "training_step": self.training_step,

            # Snapshot
            "training_config": {
                "encoding": self.config.state_encoding_dim_type,
                "encoding_flattened": self.config.state_encoding_flattened,
                "reward": self.config.online_reward_type, # Placeholder / which online vs offline do you want
            }
        }

    def _deserialize_model(self, data: bytes):
        buffer = io.BytesIO(data)
        checkpoint = torch.load(buffer)

        state_dict = checkpoint.get("policy_state")

        if state_dict is not None and hasattr(self.policy, "load_state_dict"):
            self.policy.load_state_dict(state_dict)


    def _load_metadata(self, metadata):
        if metadata is None:
            return

        # Sanity check for dumb agent / dumb training
        expected_agent = self.config.agent_type[self.player_id]

        if metadata.get("agent") != expected_agent:
            print("Warning: loading model from different agent type")
        else:
            print("Success: loading model from correct agent type")
        

        self.training_step = metadata.get("training_step", 0)


    def save(self, checkpoint=None): # Placeholder All checkpoint=None

        if self.storage is None:
            return
        
        paths = self._get_paths(checkpoint)
        
        model_bytes = self._serialize_model()
        metadata = self._build_metadata(checkpoint)

        self.storage.save_model(paths["model_path"], model_bytes)
        self.storage.save_metadata(paths["metadata_path"], metadata)

    def load(self, checkpoint=None):
        if self.storage is None:
            return
        
        paths = self._get_paths(checkpoint)

        model_bytes = self.storage.load_model(paths["model_path"])
        metadata = self.storage.load_metadata(paths["metadata_path"])

        if model_bytes is not None:
            self._deserialize_model(model_bytes)
        
        if metadata is not None:
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

        Called offline in main
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
        if self.config.debug_prints_enabled:
            print("Buffer size:", len(self.buffer))

            # Debug pipeline
            if len(self.buffer) >= self.training_batch_size:
                batch = self.buffer.sample(self.config.how_many_games) # Workaround - not great - known

                
                print("Sample batch:")
                for index, exp in enumerate(batch):
                    if index % self.config.debug_print_frequency_offline_batch == 0:
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

        if self.config.debug_prints_enabled:
            self.debug_TransitionsSteps_count += 1
            if self.debug_TransitionsSteps_count % self.config.debug_print_frequency_TransitionsSteps == 0:
                print("----------------------")
                print(f"Stored experience during transition for player {player_id}")
                print(f"[Buffer] size={len(self.buffer)} last_reward={reward} done={done}")
                

    def train_step(self):
        if len(self.buffer) < self.training_batch_size:
            return

        if self.training_step % self.config.training_step_frequency != 0:
            self. training_step += 1
            return

        batch = self.buffer.sample(self.training_batch_size)

        states = np.array([e["state"] for e in batch])
        rewards = np.array([e["reward"] for e in batch])
        dones = np.array([e["done"] for e in batch])
        action = np.array([e["action"] for e in batch])

        # Print for debug of encoding
        if self.config.debug_prints_enabled:
            print(f"[TRAIN] step={self.training_step} buffer={len(self.buffer)}")

        # Placeholder for real 'training'
        # ex. loss = model(states) vs target

        self.training_step += 1

        if self.config.model_checkpoint_enabled and self.training_step % self.config.model_checkpoint_interval == 0:
            self.save(checkpoint=f"step_{self.training_step}")