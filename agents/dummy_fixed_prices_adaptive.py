from agents import load

AlphaAgent = load('ads-annihilators/abs_agents/alpha_agent.py').AlphaAgent


class Agent(AlphaAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, initial_item0_price=0.97498204, initial_item1_price=4.19529964, **kwargs)

    def _update_decision(self):
        if self.did_customer_buy_from_me:  # can increase prices
            self.alpha *= 1.1
        else:  # should decrease prices
            self.alpha *= 0.9
