from statsmodels.stats.proportion import proportions_ztest, proportion_confint

from agents.ads_annihilators.abs_agents.base_agent import BaseAgent
from agents.ads_annihilators.abs_agents.moonshot import Moonshot


class ABTestAttr:
    def __init__(self,
                 agent: BaseAgent,
                 attribute_name,
                 attribute_test_val,
                 ab_length=1000,
                 switch_times=1,
                 ab_alpha=0.05):

        self.agent = agent
        self.ab_length = ab_length
        self.ab_alpha = ab_alpha
        self.round_number = 0
        self.switch_interval = ab_length // (switch_times * 2)

        # AB Test attribute
        self.attribute_name = attribute_name
        self.attribute_test_val = attribute_test_val
        if isinstance(agent, Moonshot):
            agent = agent.true_agent
        self.attribute_og_val = getattr(agent, attribute_name)
        self.og_profit = 0
        self.test_profit = 0

    def set_attributes(self, val):
        if isinstance(self.agent, Moonshot):
            setattr(self.agent.true_agent, self.attribute_name, val)
        else:
            setattr(self.agent, self.attribute_name, val)

    def check_significance(self):
        num_each = self.ab_length // 2
        nobs = [num_each, num_each]
        success = [self.og_profit, self.test_profit]
        z_stat, pval = proportions_ztest(success, nobs=nobs, alternative='larger')
        (lower_con, lower_treat), (upper_con, upper_treat) = proportion_confint(success, nobs=nobs, alpha=0.05)
        if pval < self.ab_alpha and lower_treat > lower_con and upper_treat > upper_con:
            # Test group is not same and has higher interval for profits
            self.set_attributes(self.attribute_test_val)
        else:
            self.set_attributes(self.attribute_og_val)

    def action(self, obs):
        if self.round_number == self.ab_length:
            self.test_profit = self.agent.profit - self.og_profit
            self.check_significance()
        elif self.round_number % self.switch_interval*2 == 0:     # finished test segment
            self.test_profit = self.agent.profit - self.og_profit
            self.set_attributes(self.attribute_og_val)
        elif self.round_number % self.switch_interval == 0:       # finished og segment (control)
            self.og_profit = self.agent.profit - self.test_profit
            self.set_attributes(self.attribute_test_val)
        # Run agent based on stage
        self.round_number += 1
        return self.agent.action(obs)
