from agents.ads_annihilators.abs_agents.base_agent import BaseAgent
from agents.ads_annihilators.abs_agents.base_opt import BaseOpt


class SingleAlphaAgent(BaseOpt):
    def __init__(self, *args,
                 initial_alpha=1.0,
                 upper_alpha_threshold=1.0,
                 upper_alpha_reset=0.99,
                 lower_alpha_threshold=0.0,
                 lower_alpha_reset=0.1,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.alphas = [initial_alpha for _ in range(self.n_items)]
        self.last_op_alphas = [initial_alpha for _ in range(self.n_items)]

        # Bounding to keep alpha in a specific range
        self.upper_alpha_threshold = upper_alpha_threshold
        self.upper_alpha_reset = upper_alpha_reset
        self.lower_alpha_threshold = lower_alpha_threshold
        self.lower_alpha_reset = lower_alpha_reset

    # Override
    def process_last_sale(self, obs):
        super().process_last_sale(obs)
        alpha = 1
        if self.round_number > 1:
            max_discount = 0
            for i in range(self.n_items):
                discount = self.last_cust_values[i] - self.op_last_prices[i]
                if discount > max_discount:
                    alpha = min(self.op_last_prices[i] / max(self.last_cust_values[i], 0.01), 1)
            self.last_op_alphas = [alpha for i in range(self.n_items)]

    def bound_alpha(self):
        for i in range(self.n_items):
            if self.alphas[i] > self.upper_alpha_threshold:
                self.alphas[i] = self.upper_alpha_reset
            elif self.alphas[i] < self.lower_alpha_threshold:
                self.alphas[i] = self.lower_alpha_reset

    def pre_action(self, obs):
        self.process_last_sale(obs)
        self.update_decision()
        self.bound_alpha()
        self.update_cust_values()

    def action(self, obs):
        # Update params and process last sale
        self.pre_action(obs)

        # Submit Prices
        if self.project_part == 1:
            return [self.current_covariates[0] * self.alphas[0] - 0.0001]
        else:
            return [self.item_prices[i] * self.alphas[i] - 0.0001 for i in range(self.n_items)]
