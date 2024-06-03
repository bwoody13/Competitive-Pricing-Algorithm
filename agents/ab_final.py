from agents.ads_annihilators.abs_agents.ab_test_agents import ABTestAgents
from agents.ads_annihilators.abs_agents.ab_test_variant_attrs import ABTestVariantAttrs
from agents.ads_annihilators.abs_agents.base_coop_exploit import BaseCoopExploit


class Agent(ABTestAgents):
    def __init__(self, *args, **kwargs):
        self.attributes = {
            "exploit_threshold": 70,
        }
        self.attributes2 = {
                "exploit_threshold": 30,
                "moonshot_threshold": 10
        }
        self.agent1 = BaseCoopExploit(*args,
                                      moonshot=True,
                                      lower_alpha_threshold=0.2,
                                      lower_alpha_reset=0.4,
                                      **kwargs)
        ab1 = ABTestVariantAttrs(self.agent1, self.attributes, ab_length=250)

        self.agent2 = BaseCoopExploit(*args,
                                      single_alpha=True,
                                      moonshot=True,
                                      lower_alpha_threshold=0.2,
                                      lower_alpha_reset=0.4,
                                      **kwargs)
        ab2 = ABTestVariantAttrs(self.agent2, self.attributes, ab_length=250)
        super().__init__(ab1, ab2, ab_length=1500, switch_times=3)

    def action(self, obs):
        if self.round_number == 500:
            self.agent1 = ABTestVariantAttrs(self.agent1, self.attributes2, ab_length=250)
            self.agent2 = ABTestVariantAttrs(self.agent2, self.attributes2, ab_length=250)
        return super().action(obs)
