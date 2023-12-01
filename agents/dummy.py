import random
from agents.ads_annihilators.abs_agents.base_agent import BaseAgent


class Agent(BaseAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, dummy=True, **kwargs)

    def action(self, obs):
        return [random.random() for _ in range(self.n_items)]
