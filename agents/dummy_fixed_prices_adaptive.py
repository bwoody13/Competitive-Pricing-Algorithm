from agents.ads_annihilators.abs_agents.base_agent import BaseAgent


class Agent(BaseAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                         initial_item0_price=0.97498204,
                         initial_item1_price=4.19529964,
                         dummy=True,
                         **kwargs)

    def update_decision(self):
        if self.did_customer_buy_from_me:  # can increase prices
            self.alphas = [self.alphas[i] * 1.1 for i in range(self.n_items)]
        else:  # should decrease prices
            self.alphas = [self.alphas[i] * 0.9 for i in range(self.n_items)]

