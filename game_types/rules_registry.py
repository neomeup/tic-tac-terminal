'''
Registry mapping to set names from config to their implementation functions.

Enables dynamic selection of game rules for CLI and simulation.
'''


# If new rule types (win/draw conditions) are created, they need to be imported and a registry entry mapped for use
## All returns are structured won game, winning player, drawn game - this pattern should be followed for new rule sets

from game_types.standard import standard_rules as game_finished

rule_registry = {
    "standard": game_finished,
}