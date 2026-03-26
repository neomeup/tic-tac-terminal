from players.computer_players.model_policy_registry import model_policy_registry


class NonAgent:
    def __init__(self, config, player_id, policy_name=None):
        if policy_name is None:
            self.policy = "sequence_policy"

        self.config = config
        self.player_id = player_id
        
        policy_class = model_policy_registry[policy_name]
        self.policy = policy_class()

    def select_action(self, player_id, board, config, rng, encoded_state=None):
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