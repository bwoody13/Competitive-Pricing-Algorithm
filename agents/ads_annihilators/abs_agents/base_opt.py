from agents.ads_annihilators.abs_agents.base_agent import BaseAgent
from agents.ads_annihilators.optimizer import Optimizer


class BaseOpt(BaseAgent):
    def __init__(self,
                 *args,
                 optimizer=None,
                 initial_item0_price=40,
                 initial_item1_price=40,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.optimizer = optimizer if optimizer else Optimizer()

        self.last_cust_values = [0.01] if self.project_part == 1 else [initial_item0_price, initial_item1_price]

        # Set item prices that are manipulated by alpha (for part 2), can also think of predicted valuations
        if self.project_part == 1:
            self.item_prices = self.last_cust_values
        else:
            self.item_prices = [initial_item0_price, initial_item1_price]

    def set_item_prices(self):
        if self.project_part == 1:
            self.item_prices = self.current_covariates
        else:
            prices, rev = self.optimizer.get_revenue_maximizing_prices_and_revenue_from_cov(self.current_covariates)
            self.item_prices = prices

    # Override
    def update_decision(self):
        self.set_item_prices()

    def update_cust_values(self):
        if self.project_part == 1:
            self.last_cust_values = self.current_covariates
        else:
            self.last_cust_values = self.item_prices
