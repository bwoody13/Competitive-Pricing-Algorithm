class ABTestAgents:
    def __init__(self,
                 agent1,
                 agent2,
                 ab_length=1000,
                 switch_times=1):
        self.agent1 = agent1
        self.agent2 = agent2
        self.curr_agent_id = 0
        self.ab_length = ab_length #ab test length
        self.switch_interval = ab_length // (switch_times * 2)

        # Params for tracking agents
        self.round_number = 0
        self.a1_profit = 0
        self.a2_profit = 0

    def switch_agents(self):
        self.curr_agent_id = 1 - self.curr_agent_id

    def action(self, obs):
        if self.round_number == self.ab_length:
            self.a1_profit = self.agent1.profit
            self.a2_profit = self.agent2.profit
            # Set best agent
            if self.a2_profit > self.a1_profit:
                self.curr_agent_id = 1
            else:
                self.curr_agent_id = 0
        elif self.round_number % self.switch_interval == 0 and self.round_number < self.ab_length:
            self.switch_agents()

        self.round_number += 1
        return self.agent1.action(obs) if self.curr_agent_id == 0 else self.agent2.action(obs)

    # def action(self, obs):
    #     # Get profit
    #     if self.round_number == self.ab_length // 2:
    #         self.a1_profit = self.agent1.profit
    #     elif self.round_number == self.ab_length:
    #         self.a2_profit = self.agent2.profit
    #         # Set best agent
    #         if self.a2_profit > self.a1_profit:
    #             self.best_agent = self.agent2
    #
    #     # Run agent based on stage
    #     if self.round_number < self.ab_length // 2:
    #         ret_val = self.agent1.action(obs)
    #     elif self.round_number < self.ab_length:
    #         ret_val = self.agent2.action(obs)
    #     else:
    #         ret_val = self.best_agent.action(obs)
    #     self.round_number += 1
    #     return ret_val
