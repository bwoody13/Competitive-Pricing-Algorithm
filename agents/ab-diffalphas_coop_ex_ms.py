from agents.ads_annihilators.abs_agents.ab_test_agents import ABTestAgents
from agents.ads_annihilators.abs_agents.base_coop_exploit import BaseCoopExploit


class Agent(ABTestAgents):
    def __init__(self, *args, **kwargs):
        agent1 = BaseCoopExploit(*args,
                                 moonshot=True,
                                 lower_alpha_threshold=0.2,
                                 lower_alpha_reset=0.4,
                                 **kwargs)
        agent2 = BaseCoopExploit(*args,
                                 single_alpha=True,
                                 exploit_threshold=75,
                                 **kwargs)
        super().__init__(agent1, agent2)
