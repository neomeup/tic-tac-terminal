import random

from core.game_state import GameState
from core.run_context import GameRunContext
from core.serialization import serialize_board
from game_engine.board_build import build_starting_board
from game_engine.apply_move import apply_move
from game_types.used_rules import game_finished
from simulation.result import SimulationResult


from movement.computer_players.computer_movement import get_computer_move, get_agent
from simulation.rewards.reward_registry import reward_registry



from simulation.training.encoding.encoder_registry import encoder_registry

# Probably leave unregisterized - if you need better action encoding, just change encode action
from simulation.training.encoding.encoders.action_encoder import encode_action


class SimulationEngine:

    # Top constructor
    def __init__(self, config):
        self.config = config
        self.total_players = len(config.player_types)

        if self.config.random_seed is not None:
            self.rng = random.Random(self.config.random_seed)
        else:
            self.rng = random.Random()

        reward_class = reward_registry[self.config.reward_type]
        self.reward_engine = reward_class()

        encoder_class = encoder_registry[self.config.state_encoding_dim_type]
        self.encoder = encoder_class()

    # Helper function for encoding
    def _encode_board(self, board_state, player_id):

        flat, matrix = self.encoder.compute_encode(board_state, player_id)

        if self.config.state_encoding_flattened:
            return flat
        else: 
            return matrix

    # Public Methods
    def run(self) -> SimulationResult:
        game_history = []

        for _game_index in range(self.config.how_many_games):
            context = self._run_single_game()
            print("------------")
            game_history.append(context)

        return SimulationResult(game_history)


    # Single Game Execution
    def _run_single_game(self) -> GameRunContext:

        state = self._initialize_state()
        context = self._initialize_run_context()

        context.log_move(
            turn_number=0,
            player_id=None,
            board_state=serialize_board(state.board),
            action=None,
            reward=None
        )

        print("Starting player:", state.current_player_id) # Debug random_seed

        while not state.is_finished:
            self._step(state, context)

        return context


    ## Initialization
    # Initialize Starting Board
    def _initialize_state(self) -> GameState:
        board = build_starting_board(self.config.board_size)

        state = GameState(
            board=board,
            players=list(range(self.total_players)),
            config=self.config
        )

        if self.config.random_start:
            state.current_player_id = self.rng.randint(0, self.total_players - 1)
        else:
            state.current_player_id = 0

        return state

    # Initialize Logging and Metadata
    def _initialize_run_context(self) -> GameRunContext:
        context = GameRunContext(vars(self.config).copy())

        for player_id, player_type in enumerate(self.config.player_types):
            context.register_player(
                player_id=player_id,
                player_type=player_type,
                model_version=self.config.model_type[player_id]
            )

        return context



    ## Core loop logic called by and controlled by run single game - performs a single turn
    # Allow separation of action/policy choice 
    def _choose_action(self, state: GameState):
        return get_computer_move(
            state.current_player_id,
            state.board,
            self.config,
            self.rng
        )
    
    # Perform the step based on current action/policy
    def _step(self, state: GameState, context: GameRunContext):

        # Capture state before action
        previous_state = serialize_board(state.board)

        move = self._choose_action(state)

        new_board, valid_move = apply_move(move, state.board, self.config)

        # Possible implementation of a penalty or something for non valid move
        if not valid_move:
            pass

        if valid_move:
            state.board = new_board

            state.turn_number += 1

            # Check game termination
            won, winner, draw = game_finished(self.config, state.board)

            if won:
                state.is_finished = True
            elif draw:
                state.is_finished = True

            reward = self.reward_engine.compute_reward(
                player_id=move.player_id,
                winner=winner,
                draw=draw,
                board_state=state.board,
                move=move
            )

            next_state = serialize_board(state.board)

            if self.config.online_training_enabled:
                agent = get_agent(move.player_id, self.config)

                print(
                    "RL TRANSITION:",
                    "Player:", move.player_id,
                    "Reward:", reward,
                    "Done:", state.is_finished
                )


                board_size = len(previous_state)

                encoded_state = self._encode_board(previous_state, move.player_id)
                encoded_next_state = self._encode_board(next_state, move.player_id)

                encoded_action = encode_action(
                    {"row": move.target_row, "col": move.target_col},
                    board_size
                )


                agent.observe_transition(
                    state=encoded_state,
                    action=encoded_action,
                    reward=reward,
                    next_state=encoded_next_state,
                    done=state.is_finished,
                    player_id=move.player_id
                )

                agent.train_step()

            context.log_move(
                turn_number=state.turn_number,
                player_id=move.player_id,
                board_state=serialize_board(state.board),
                action={
                    "row": move.target_row,
                    "col": move.target_col
                },
                reward=reward
            )

            if won:
                if self.config.online_training_enabled:
                    for player_id in range(self.total_players):

                        if player_id == move.player_id:
                            continue

                        loser_agent = get_agent(player_id, self.config)

                        if loser_agent is None:
                            continue

                        loser_state = self._encode_board(next_state, player_id)

                        loser_agent.observe_transition(
                            state=loser_state,
                            action=None,
                            reward=-1.0,
                            next_state=loser_state,
                            done=True,
                            player_id=player_id
                        )
                context.finalize(winner=winner, draw=False)

            elif draw:
                state.is_finished = True
                context.finalize(winner=None, draw=True)


            state.current_player_id = (
                state.current_player_id + 1
            ) % self.total_players