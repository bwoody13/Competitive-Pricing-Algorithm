import random
from agents import load

BaseAgent = load('ads-annihilators/abs_agents/base_agent.py').BaseAgent


class Agent(BaseAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def action(self, obs):
        return [random.random() for _ in range(self.n_items)]
