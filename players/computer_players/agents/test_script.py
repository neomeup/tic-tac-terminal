from config import GameConfig
from players.computer_players.agents.rl_dumb_agent import RLDumbAgent

test_config = GameConfig()

agent = RLDumbAgent(config=test_config, player_id=0)

# ---- TEST SAVE ----
agent.save(checkpoint="step_1")

# ---- TEST LOAD ----
agent.load(checkpoint="step_1")

print("Done")