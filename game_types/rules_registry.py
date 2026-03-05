'''
Registry for the different algorithms 
'''

from game_types.standard import standard_rules as game_finished

rule_registry = {
    "standard": game_finished,
}