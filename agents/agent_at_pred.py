from agents.ads_annihilators.abs_agents.base_agent import BaseAgent


class Agent(BaseAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def action(self, obs):
        self.process_last_sale(obs)
        self.update_decision()
        self.update_cust_values()
        return [self.item_prices[i] - 0.001 for i in range(self.n_items)]


