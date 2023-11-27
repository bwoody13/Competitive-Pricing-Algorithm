from agents.ads_annihilators.abs_agents.base_agent import BaseAgent


class AlphaAgent(BaseAgent):
    def __init__(self, *args, initial_alpha=1.0, initial_item0_price=40, initial_item1_price=40, **kwargs):
        super().__init__(*args, **kwargs)
        self.alpha = initial_alpha

        # Set item prices that are manipulated by alpha (for part 2)
        self.item0_price = initial_item0_price
        self.item1_price = initial_item1_price

    def action(self, obs):
        # Update params and process last sale
        self.process_last_sale(obs)
        self.update_decision()

        # Submit Prices
        if self.project_part == 1:
            return [self.current_covariates[0] * self.alpha - 0.0001]
        else:
            return [self.item0_price * self.alpha - 0.0001, self.item1_price * self.alpha - 0.0001]