'''
Registry for RL/AI agents
'''
from players.computer_players.policies.random_policy import RandomPolicy # Non agent policy thus pass policy directly
from players.computer_players.agents.rl_dumb_agent import RLDumbAgent


# Class for random agent as it is passed directly
class RandomAgent:
    def __init__(self, policy_name=None):
        self.policy = RandomPolicy()

    def select_action(self, player_id, board, config, rng):
        return self.policy.select_action(
            player_id,
            board,
            config,
            rng
        )

    def observe(self, *args, **kwargs):
        pass

    def observe_transition(self, *args, **kwargs):
        pass

    def train_step(self):
        pass


agent_registry = {
    "rl_dumb_agent": RLDumbAgent,
    "random_agent": RandomAgent
}