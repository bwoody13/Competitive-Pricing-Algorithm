import sys
from agents.ads_annihilators.abs_agents.base_agent import BaseAgent
from agents.ads_annihilators.abs_agents.base_opt import BaseOpt

import numpy as np


class Moonshot(BaseAgent):
    def __init__(self, *args,
                 moonshot_threshold=6.5,
                 moonshot_percent=0.2,
                 true_agent: BaseOpt = None,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.true_agent = true_agent
        self.moonshot_threshold = moonshot_threshold
        self.moonshot_percent = moonshot_percent

    # Override
    def action(self, obs):
        action = self.true_agent.action(obs)
        for i in range(self.n_items):
            if np.random.rand() < self.moonshot_percent and self.true_agent.item_prices[i] < self.moonshot_threshold:
                action[i] = sys.maxsize
        return action

    # # Override
    # def __getattr__(self, item):
    #     if item in self.__dict__:
    #         return self.__dict__[item]
    #     return getattr(self.true_agent, item)
    #
    # # Override
    # def __setattr__(self, key, value):
    #     if key in self.__dict__ or key in ['true_agent', 'moonshot_threshold', 'moonshot_percent']:
    #         super().__setattr__(key, value)
    #     else:
    #         setattr(self.true_agent, key, value)
