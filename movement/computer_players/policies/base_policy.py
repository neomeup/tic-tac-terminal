class BasePolicy:

    def select_action(self, player_id, board, config, rng):
        raise NotImplementedError