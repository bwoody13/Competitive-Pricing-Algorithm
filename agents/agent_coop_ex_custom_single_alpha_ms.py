from agents.ads_annihilators.abs_agents.single_alpha_base_coop_exploit_ms import SingleAlphaCoopExploitMS


class Agent(SingleAlphaCoopExploitMS):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                         exploit_threshold=75,
                         **kwargs)
