'''
Registry for the different movement inputs
'''

from players.human_players.cli_human import get_cli_move as cli_move

human_move_registry = {
    "cli": cli_move,
}