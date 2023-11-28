import sys
from agents.ads_annihilators.abs_agents.base_agent import BaseAgent


class Agent(BaseAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def action(self, obs):
        return [sys.maxsize for _ in range(self.n_items)]
