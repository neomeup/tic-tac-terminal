import curses
import time
import random

from game_engine.board_build import build_starting_board
from game_engine.apply_move import apply_move
from core.move import Move

from renderers.cli_renderer import render_board, render_game_draw, render_game_won
from game_types.used_rules import game_finished

from movement.human_players.human_movement import get_player_move
from movement.computer_players.computer_movement import get_computer_move


class CLIRuntime:

    # Top constructor CLI
    def __init__(self, config):
        self.config = config
        self.total_players = len(config.player_types)
        self.is_all_computer = all(player == "computer" for player in self.config.player_types)
        
        if self.config.random_seed is not None:
            self.rng = random.Random(self.config.random_seed)
        else:
            self.rng = random.Random()

    # Public Methods entry
    def run(self, stdscr):

        self._setup_curses(stdscr)

        size = self.config.board_size
        game_count = 1

        game_running = True
        build_new_game = True

        while True:

            stdscr.clear()

            # New Game Setup
            if build_new_game:
                board_lst = build_starting_board(size)

                player_1_pos = [0, 0]
                player_2_pos = [0, size - 1]

                if self.config.random_start:
                    current_player_index = self.rng.randint(0, self.total_players - 1)
                else:
                    current_player_index = 0

                build_new_game = False

            # Rendering
            if game_running:
                board_lst = render_board(
                    stdscr,
                    self.config,
                    tuple(player_1_pos),
                    tuple(player_2_pos),
                    board_lst,
                    current_player_index,
                    game_count
                )

                won, winner, draw = game_finished(self.config, board_lst)

                if won:
                    render_game_won(stdscr, self.config, winner, board_lst, game_count)
                    game_running = False

                elif draw:
                    render_game_draw(stdscr, self.config, board_lst, game_count)
                    game_running = False


            # Computer control if not fully human game
            current_player_type = self.config.player_types[current_player_index]

            if current_player_type == "computer" and game_running:

                time.sleep(1)

                move = get_computer_move(
                    current_player_index,
                    board_lst,
                    self.config,
                    self.rng
                )

                board_lst, changed_flag = apply_move(move, board_lst, self.config)

                if changed_flag:
                    current_player_index = (current_player_index + 1) % self.total_players

            # Repeat games for computer vs computer
            elif not game_running and self.is_all_computer:
                time.sleep(3)

                if game_count >= self.config.how_many_games:
                    break

                game_count += 1
                game_running = True
                build_new_game = True


            # Human control
            else:

                key = stdscr.getch()

                # Quits
                if key == ord("q"):
                    if current_player_index == 0 or not game_running:
                        break
                elif key == ord("/"):
                    if current_player_index == 1 or not game_running:
                        break
                
                # New Game
                elif key == ord("n"):
                    if not game_running:
                        build_new_game = True
                        game_running = True

                # Adjust for terminal resize
                elif key == curses.KEY_RESIZE:
                    continue
                
                # Movement keys
                elif key in [
                    ord("w"), ord("a"), ord("s"), ord("d"),
                    curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT
                ]:

                    if current_player_index == 0:
                        player_1_pos = get_player_move(
                            key,
                            current_player_index,
                            player_1_pos,
                            size,
                            self.config
                        )

                    elif current_player_index == 1:
                        player_2_pos = get_player_move(
                            key,
                            current_player_index,
                            player_2_pos,
                            size,
                            self.config
                        )

                # Selection keys
                elif key == ord("e"):
                    if current_player_index == 0:
                        move = Move(
                            player_id=current_player_index,
                            target_row=player_1_pos[0],
                            target_col=player_1_pos[1]
                        )
                        board_lst, changed_flag = apply_move(move, board_lst, self.config)
                        if changed_flag is True:
                            current_player_index = (current_player_index + 1) % self.total_players
                elif key in [curses.KEY_ENTER, 10, 13]:
                    if current_player_index == 1:
                        move = Move(
                            player_id=current_player_index,
                            target_row=player_2_pos[0],
                            target_col=player_2_pos[1]
                        )
                        board_lst, changed_flag = apply_move(move, board_lst, self.config)
                        if changed_flag is True:
                            current_player_index = (current_player_index + 1) % self.total_players

    # ------------------------

    def _setup_curses(self, stdscr):

        stdscr.clear()
        curses.curs_set(0)
        stdscr.nodelay(False)
        stdscr.keypad(True)
        curses.noecho()

        if curses.has_colors():
            curses.start_color()
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
            curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)
            curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)

            stdscr.bkgd(' ', curses.color_pair(1))
            stdscr.clear()