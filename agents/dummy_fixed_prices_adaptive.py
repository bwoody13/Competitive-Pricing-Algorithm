from agents.ads_annihilators.abs_agents.alpha_agent import AlphaAgent


class Agent(AlphaAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, initial_item0_price=0.97498204, initial_item1_price=4.19529964, **kwargs)

    def update_decision(self):
        if self.did_customer_buy_from_me:  # can increase prices
            self.alphas = [self.alphas[i] * 1.1 for i in range(self.n_items)]
        else:  # should decrease prices
            self.alphas = [self.alphas[i] * 0.9it  for i in range(self.n_items)]
