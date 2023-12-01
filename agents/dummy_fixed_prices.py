import random
from agents.ads_annihilators.abs_agents.base_agent import BaseAgent


class Agent(BaseAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, dummy=True, **kwargs)

    def action(self, obs):
        new_buyer_covariates, _, _ = obs

        if self.project_part == 1:
            # just return customer valuation, which would be optimal if there was no competitor
            return [new_buyer_covariates[0] - .0001]
        else:
            return [0.97498204, 4.19529964][0:self.n_items]
