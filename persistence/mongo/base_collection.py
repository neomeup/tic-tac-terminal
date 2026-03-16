from typing import TypedDict, Literal, Any
from datetime import datetime


class ExperienceStep(TypedDict):
    turn: int

    state: list[list[dict[str, Any] | None]]
    action: dict[str, int] | None
    reward: float | None
    next_state: list[list[dict[str, Any] | None]]
    done: bool

    player_id: int | None

    policy: str | None
    policy_version: str | None

    agent: str | None
    agent_version: str | None

    exploration_rate: float | None
    action_source: Literal["exploration", "policy"] | None

class SimulationExperienceDocument(TypedDict):
  
    simulation_run_id: int
    game_id: int
    player_ids: list[int]

    winning_player: int | None
    drawn_game: bool

    encoder: str
    flat_encoding: bool

    experiences: list[ExperienceStep]

    created_at: datetime
