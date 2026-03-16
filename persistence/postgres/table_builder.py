'''
Format data from SimulationResults GameRunContext and build payloads for insertion to postgres
'''

from typing import Any
from simulation.result import SimulationResult

def build_postgres_payloads(result: SimulationResult, config) -> dict[str, Any]:

    # Simulation run info
    simulation_payload = {
        "rule_set": config.rule_set,
        "encoder": config.state_encoding_dim_type,
        "reward_system": config.online_reward_type,
        "num_games": len(result.runs),
        "config_json": vars(config),
    }

    # Players info
    players_payload = []
    for player_id, player_type in enumerate(config.player_types):
        agent_name = config.agent_type[player_id] if player_type != "human" else None
        policy_name = config.policy_type[player_id] if player_type != "human" else None

        players_payload.append({
            "internal_id": player_id,  # for mapping moves later
            "account_user": "local_neal", # Placeholder for when a users db exists
            "player_type": player_type,
            "agent_name": agent_name,
            "agent_version": "v1" if agent_name else None, # Placeholder for when versioning exists
            "policy_name": policy_name,
            "policy_version": "v1" if policy_name else None, # Placeholder for when versioning exists
        })

    # Games + moves
    games_payload = []
    for game in result.runs:

        moves_payload = []
        for move in game.moves:
            moves_payload.append({
                "turn": move["turn_number"],
                "player_id_in_game": move["player_id"],
                "row": move["action"]["row"] if move["action"] else None,
                "col": move["action"]["col"] if move["action"] else None,
                "reward": move["reward"] if move["reward"] else None,
                "board_state": move["board_state"]
            })

        games_payload.append({
            "winner": game.winner,
            "draw": game.draw,
            "moves": moves_payload
        })

    return {
        "simulation": simulation_payload,
        "players": players_payload,
        "games": games_payload
    }