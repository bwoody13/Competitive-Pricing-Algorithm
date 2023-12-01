from agents.ads_annihilators.abs_agents.base_coop_exploit import BaseCoopExploit


class Agent(BaseCoopExploit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                         moonshot=True,
                         lower_alpha_threshold=0.5,
                         lower_alpha_reset=0.75,
                         **kwargs)
