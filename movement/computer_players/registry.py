'''
Registry for the different algorithms 
'''

from movement.computer_players.com_random import get_move as random_move

computer_move_registry = {
    "random": random_move,
}