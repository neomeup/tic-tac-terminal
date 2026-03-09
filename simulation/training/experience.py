'''
Defines Experience dataclass for RL agents.
'''

from dataclasses import dataclass
from typing import Any

@dataclass
class Experience:
    state: Any
    action: Any
    reward: float
    next_state: Any
    done: bool
    player_id: int