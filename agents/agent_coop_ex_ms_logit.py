from agents.ads_annihilators.abs_agents.base_coop_exploit import BaseCoopExploit
from agents.ads_annihilators.optimizer import Optimizer


class Agent(BaseCoopExploit):
    def __init__(self, *args, **kwargs):
        opt = Optimizer("agents/ads_annihilators/logit_v1.pkl")
        super().__init__(*args,
                         moonshot=True,
                         lower_alpha_threshold=0.2,
                         lower_alpha_reset=0.4,
                         **kwargs)
