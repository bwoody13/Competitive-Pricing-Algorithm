from agents.ads_annihilators.abs_agents.single_alpha_base_coop_exploit import SingleAlphaBaseCoopExploit


class Agent(SingleAlphaBaseCoopExploit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                         exploit_threshold=75,
                         **kwargs)
