'''
Q-learning policy implementation.

Stores Q-values in a table and updates based on experience.
'''

from core.move import Move
from players.computer_players.policies.base_policy import BasePolicy
from simulation.training.encoding.encoders.action_encoder import encode_action, decode_action


from debugging_testing.printing_debug import dbprint

class QLearningPolicy(BasePolicy):
    # alpha = learning rate, gamma = discount factor, epsilon = exploration vs exploitation
    def __init__(self, alpha=0.1, gamma=0.99, epsilon=0.005):
        self.q_table = {}

        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon # decay epsilon automatically after


        debug_print = False
        self.dbprint = lambda *args, **kwargs: dbprint(debug_print, *args, **kwargs)

    def _get_q(self, state_key, action):
        return self.q_table.get((state_key, action), 0.0)

    def select_action(self, player_id, board, config, rng, encoded_state=None):

        self.dbprint("------start select action------")
        self.dbprint("Player id of turn: ", player_id)
        # encode for q table
        if encoded_state is None:
            raise ValueError("QLearningPolicy requires encoded state")

        # change to str for hashing
        self.dbprint("pre-string state: ", encoded_state)
        state_key = tuple(encoded_state.tolist())

        self.dbprint("state key: ", state_key)
        
        possible_actions = []
        for r, row in enumerate(board):
            for c, cell in enumerate(row):
                if cell is None:
                    action = encode_action(None, config.board_size, r, c)
                    possible_actions.append(action)
        
        # epsilon-greedy
        if rng.random() < self.epsilon:
            action = rng.choice(possible_actions)
            q = self._get_q(state_key, action)
            self.dbprint("Less than epsilon action, action: ", action)
        else:
            best_value = float("-inf")
            action = None

            for a in possible_actions:
                q = self.q_table.get((state_key, a), 0.0)
                if q > best_value:
                    best_value = q
                    action = a
            self.dbprint("Get q > action, action: ", action)
            self.dbprint("Best value: ", best_value)
            if action is None:
                action = rng.choice(possible_actions)
                self.dbprint("None action, action: ", action)

        # decode for Move
        row, col = decode_action(action, config.board_size)

        self.dbprint("q: ", q)
        #self.dbprint("q table: ", self.q_table)
        self.dbprint("end select action")

        return Move(player_id=player_id, target_row=row, target_col=col)

    def update(self, state, action, reward, next_state, done, size):
        self.dbprint("start update")
        state_key = tuple(state.tolist())
        self.dbprint("state key: ", state_key)

        self.dbprint("reward: ", reward)
        self.dbprint("done: ", done)
        
        next_state_inverted = - next_state

        next_state_key = tuple(next_state_inverted.tolist())
        self.dbprint("next state key: ", next_state_key)
        
        current_q = self._get_q(state_key, action)
        self.dbprint("current q: ", current_q)

        possible_actions = []

        for i in range(size * size): # works because action is encoded as an index - if changed to encompass multiple piece types for example, this needs to change
            if next_state[i] == 0:  # empty cell
                possible_actions.append(i)

        future_qs = [
            self._get_q(next_state_key, a)
            for a in possible_actions
        ]

        max_future_q = max(future_qs) if future_qs else 0.0
        self.dbprint("max future: ", max_future_q)
        target = reward if done else reward - (self.gamma * max_future_q)
        self.dbprint("target: ", target)

        new_q = round( ((1 - self.alpha) * current_q) + (self.alpha * target), 6)
        self.dbprint("new q: ", new_q)
        self.q_table[(state_key, action)] = new_q
        
        self.dbprint("------end update------\n")
