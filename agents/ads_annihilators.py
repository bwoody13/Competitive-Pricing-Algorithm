from agents.ads_annihilators.abs_agents.base_coop_exploit_ms import BaseCoopExploitMS


class Agent(BaseCoopExploitMS):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                         lower_alpha_threshold=0.2,
                         lower_alpha_reset=0.4,
                         **kwargs)
