from agents.ads_annihilators.abs_agents.base_coop_exploit_ms import BaseCoopExploitMS


class Agent(BaseCoopExploitMS):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                         lower_alpha_reset=0.6,
                         moonshot_percent=0.4,
                         **kwargs)
