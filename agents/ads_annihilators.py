from agents.ads_annihilators.abs_agents.ab_test_agents import ABTestAgents
from agents.ads_annihilators.abs_agents.ab_test_variant_attrs import ABTestVariantAttrs
from agents.ads_annihilators.abs_agents.base_coop_exploit import BaseCoopExploit


class Agent(ABTestAgents):
    def __init__(self, *args, **kwargs):
        attributes = {
            "exploit_threshold": 70,
            "moonshot_threshold": 10
        }
        agent1 = BaseCoopExploit(*args,
                                 moonshot=True,
                                 lower_alpha_threshold=0.2,
                                 lower_alpha_reset=0.4,
                                 exploit_threshold=40,
                                 **kwargs)
        ab1 = ABTestVariantAttrs(agent1, attributes, ab_length=250)

        agent2 = BaseCoopExploit(*args,
                                 single_alpha=True,
                                 moonshot=True,
                                 lower_alpha_threshold=0.2,
                                 lower_alpha_reset=0.4,
                                 **kwargs)
        ab2 = ABTestVariantAttrs(agent2, attributes, ab_length=250)
        super().__init__(ab1, ab2, ab_length=1000, switch_times=2)

