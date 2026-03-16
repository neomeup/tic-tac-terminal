from persistence.mongo.base_collection import SimulationExperienceDocument
from persistence.mongo.base_collection import ExperienceStep


def build_experience_document(context, simulation_run_id: int, game_id: int, config) -> SimulationExperienceDocument:

    experiences: list[ExperienceStep] = []

    moves = context.moves

    for i in range(len(moves) - 1):

        current_move = moves[i]
        next_move = moves[i + 1]

        if current_move["player_id"] is None:
            experiences.append({
                "turn": current_move["turn_number"],

                "state": current_move["board_state"],
                "action": None,
                "reward": None,
                "next_state": next_move["board_state"],
                "done": next_move["done"],

                "player_id": None,

                "policy": None,
                "policy_version": None,

                "agent": None,
                "agent_version": None,
                
                "exploration_rate": None,
                "action_source": None
            })
            continue

        experiences.append({
            "turn": current_move["turn_number"],

            "state": current_move["board_state"],
            "action": current_move["action"],
            "reward": current_move["reward"],
            "next_state": next_move["board_state"],
            "done": next_move["done"],

            "player_id": current_move["player_id"],

            "policy": config.policy_type[current_move["player_id"]],
            "policy_version": "v1", # Placeholder for future versioning

            "agent": config.agent_type[current_move["player_id"]],
            "agent_version": "v1", # Placeholder for future versioning

            "exploration_rate": .5,  ## Placeholder for a future config.exploration_rate variable
            "action_source": "policy" ## Also placeholder
        })

    return {
        "simulation_run_id": simulation_run_id,
        "game_id": game_id,
        "player_ids": list(context.players.keys()),

        "winning_player": context.winner,
        "drawn_game": context.draw,

        "encoder": config.state_encoding_dim_type,
        "flat_encoding": config.state_encoding_flattened,

        "experiences": experiences
    }