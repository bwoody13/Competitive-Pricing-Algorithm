from agents.ads_annihilators.abs_agents.base_coop_exploit import BaseCoopExploit


class Agent(BaseCoopExploit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                         lower_alpha_threshold=0.2,
                         lower_alpha_reset=0.4,
                         moonshot_percent=0.4,
                         **kwargs)
