import random
from agents import load

BaseAgent = load('ads-annihilators/abs_agents/base_agent.py').BaseAgent


class Agent(BaseAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def action(self, obs):
        new_buyer_covariates, _, _ = obs

        if self.project_part == 1:
            # just return customer valuation, which would be optimal if there was no competitor
            return [new_buyer_covariates[0] - .0001]
        else:
            return [0.97498204, 4.19529964][0:self.n_items]
