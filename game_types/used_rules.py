'''
Computer movement middle man for main and registry
'''

from game_types.registry import rule_registry

def game_finished(config, board_lst: list[list[tuple[bool, bool, int]]]) -> tuple[bool, bool, bool]:
    rule_name = config.rule_set
    rule_function = rule_registry[rule_name]
    return rule_function(config, board_lst)