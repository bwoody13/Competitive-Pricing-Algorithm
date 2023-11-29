from agents.ads_annihilators.abs_agents.base_opt import BaseOpt


class ABTestAgents:
    def __init__(self, agent1: BaseOpt, agent2: BaseOpt, ab_length=1000):
        self.agent1 = agent1
        self.agent2 = agent2
        self.best_agent = agent1
        self.ab_length = ab_length

        # Params for tracking agents
        self.round_number = 0
        self.a1_profit = 0
        self.a2_profit = 0

    def action(self, obs):
        # Get profit
        if self.round_number == self.ab_length // 2:
            self.a1_profit = self.agent1.profit
        elif self.round_number == self.ab_length:
            self.a2_profit = self.agent2.profit
            # Set best agent
            if self.a2_profit > self.a1_profit:
                self.best_agent = self.agent2

        # Run agent based on stage
        if self.round_number < self.ab_length // 2:
            ret_val = self.agent1.action(obs)
        elif self.round_number < self.ab_length:
            ret_val = self.agent2.action(obs)
        else:
            ret_val = self.best_agent.action(obs)
        self.round_number += 1
        return ret_val
