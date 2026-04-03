'''
Wrapper between computer player moves and main game logic.
'''

from players.computer_players.agent_registry import agent_registry


# persistent agents
_agents = {}


def get_agent(player_id, config):

    if player_id not in _agents:

        agent_name = config.agent_type[player_id]
        policy_name = config.policy_type[player_id]

        agent_class = agent_registry[agent_name]

        # support for both agents with and without policy args
        try:
            _agents[player_id] = agent_class(
                config=config,
                player_id=player_id,
                policy_name=policy_name
            )
        except TypeError:
            _agents[player_id] = agent_class()

    return _agents[player_id]


def get_computer_move(current_player_index, board_lst, config, rng, encoded_state=None):

    agent = get_agent(current_player_index, config)

    return agent.select_action(
        current_player_index,
        board_lst,
        config,
        rng,
        encoded_state
    )

def offline_agent(config):
    agent_name = config.offline_agent

    agent_class = agent_registry[agent_name]
    print(agent_class)
    return agent_class(config=config, player_id=0, offline=True)