from statsmodels.stats.proportion import proportions_ztest, proportion_confint


class ABTestAttr:
    def __init__(self,
                 agent,
                 attribute_name,
                 attribute_test_val,
                 ab_length=1000):

        self.agent = agent
        self.ab_length = ab_length

        # AB Test attribute
        self.attribute_name = attribute_name
        self.attribute_test_val = attribute_test_val
        self.attribute_og_val = getattr(agent, attribute_name)

    def check_significance(self):
        num_each = self.ab_length // 2
        nobs = [num_each, num_each]
        success = [self.og_profit, self.test_profit]
        z_stat, pval = proportions_ztest(success, nobs=nobs, alternative='larger')


    def action(self, obs):
        # Get profit
        if self.round_number == self.ab_length // 2:
            self.og_profit = self.agent.profit
            setattr(self.agent, self.attribute_name, self.attribute_test_val)
        elif self.round_number == self.ab_length:
            self.test_profit = self.agent.profit - self.og_profit
            # Set best attribute
            # if self.a2_profit > self.a1_profit:
            #     self.best_agent = self.agent2

        # Run agent based on stage
        if self.round_number < self.ab_length // 2:
            ret_val = self.agent1.action(obs)
        elif self.round_number < self.ab_length:
            ret_val = self.agent2.action(obs)
        else:
            ret_val = self.best_agent.action(obs)
        self.round_number += 1
        return ret_val