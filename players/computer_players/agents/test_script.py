from config import GameConfig
from players.computer_players.agents.rl_dumb_agent import RLDumbAgent

test_config = GameConfig()

agent = RLDumbAgent(config=test_config, player_id=0)

# ---- TEST SAVE ----
agent.save()

# ---- TEST LOAD ----
agent.load()

print("Done")