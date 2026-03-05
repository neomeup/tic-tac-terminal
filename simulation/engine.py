import random

from core.game_state import GameState
from core.run_context import GameRunContext
from core.serialization import serialize_board
from game_engine.board_build import build_starting_board
from game_engine.apply_move import apply_move
from game_types.used_rules import game_finished
from simulation.result import SimulationResult

# Import for the basic move
from movement.computer_players.computer_movement import get_computer_move

# Imports for agents ** Should be registerized with a model agent registery/agent registery
from movement.computer_players.agents.rl_dumb_agent import agent as rl_agent


class SimulationEngine:

    # Top constructor
    def __init__(self, config):
        self.config = config
        self.total_players = len(config.player_types)

        if self.config.random_seed is not None:
            self.rng = random.Random(self.config.random_seed)
        else:
            self.rng = random.Random()


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

            reward = 0.0

            if won:
                if winner == move.player_id:
                    state.is_finished = True
                    reward = 1.0
                else: 
                    state.is_finished = True
                    reward = -1.0
            elif draw:
                state.is_finished = True
                reward = 0.0

            next_state = serialize_board(state.board)

            done = won or draw

            if self.config.online_training_enabled:

                print(
                    "RL TRANSITION:",
                    "Player:", move.player_id,
                    "Reward:", reward,
                    "Done:", state.is_finished
                )


                rl_agent.observe_transition(
                    state=previous_state,
                    action={
                        "row": move.target_row,
                        "col": move.target_col
                    },
                    reward=reward,
                    next_state=next_state,
                    done=state.is_finished,
                    player_id=move.player_id
                )

                rl_agent.train_step()

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
         
            state.current_player_id = (
                state.current_player_id + 1
            ) % self.total_players

            if won:
                context.finalize(winner=winner, draw=False)

            elif draw:
                state.is_finished = True
                context.finalize(winner=None, draw=True)