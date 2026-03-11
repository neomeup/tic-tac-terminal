from typing import TypedDict, Literal, Any
from datetime import datetime


class ExperienceStep(TypedDict):
    turn: int

    state: list[list[dict[str, Any] | None]]
    action: dict[str, int]
    reward: float
    next_state: list[list[dict[str, Any] | None]]
    done: bool

    policy: str
    policy_version: str

    agent: str
    agent_version: str

    exploration_rate: float
    action_source: Literal["exploration", "policy"]

class SimulationExperienceDocument(TypedDict):
  
    simulation_run_id: int
    game_id: int
    player_ids: list[int]

    encoder: str
    flat_encoding: bool

    experiences: list[ExperienceStep]

    created_at: datetime
