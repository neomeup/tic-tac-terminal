'''
Registry for reinforcement learning agents.

Maps player IDs to agent instances for online or offline training.

RandomAgent allows for RandomPolicy to still be used despite not having an agent
'''
from players.computer_players.agents.non_agent import NonAgent
from players.computer_players.agents.rl_dumb_agent import RLDumbAgent
from players.computer_players.agents.q_learning_agent import QLearningAgent


agent_registry = {
    "rl_dumb_agent": RLDumbAgent,
    "non_agent": NonAgent,
    "q_learning_agent": QLearningAgent
}