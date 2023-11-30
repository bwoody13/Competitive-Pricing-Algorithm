# This is the base level agent behaviour which every agent is a subclass of.
import sys
import numpy as np
from agents.ads_annihilators.optimizer import Optimizer


# This is now combined with Opt and Alpha agent (and single logic also mixed in)
class BaseAgent(object):
    def __init__(self,
                 agent_number,
                 params={},
                 dummy=False,
                 optimizer=None,
                 initial_item0_price=40,
                 initial_item1_price=40,
                 single_alpha=False,
                 initial_alpha=1.0,
                 upper_alpha_threshold=1.0,
                 upper_alpha_reset=0.99,
                 lower_alpha_threshold=0.0,
                 lower_alpha_reset=0.1,
                 moonshot=False,
                 moonshot_threshold=6.5,
                 moonshot_percent=0.2,
                 **kwargs):
        self.this_agent_number = agent_number  # index for this agent
        self.op_number = 1 - agent_number
        self.n_items = params["n_items"]
        self.project_part = params['project_part'] # useful to be able to use same competition code for each project part

        # Last sale information
        self.round_number = 0
        self.did_customer_buy_from_me = True
        self.item_bought = 0
        self.profit = 0
        self.op_profit = 0
        self.last_prices = [0.01, 0.01]
        self.op_last_prices = [0.01, 0.01]
        self.last_covariates = [0.01, 0.01, 0.01]

        # Current customer information (used in predictions)
        self.current_covariates = [0.01, 0.01, 0.01]

        # Intialize alpha params
        self.single_alpha = single_alpha
        self.alphas = [initial_alpha for _ in range(self.n_items)]
        self.last_op_alphas = [initial_alpha for _ in range(self.n_items)]

        # Bounding to keep alpha in a specific range
        self.upper_alpha_threshold = upper_alpha_threshold
        self.upper_alpha_reset = upper_alpha_reset
        self.lower_alpha_threshold = lower_alpha_threshold
        self.lower_alpha_reset = lower_alpha_reset

        # Set optimizer if not a dummy
        if not dummy:
            self.optimizer = optimizer if optimizer else Optimizer()
        else:
            self.optimizer = None

        self.last_cust_values = [0.01] if self.project_part == 1 else [initial_item0_price, initial_item1_price]

        # Set item prices that are manipulated by alpha (for part 2), can also think of predicted valuations
        if self.project_part == 1:
            self.item_prices = self.last_cust_values
        else:
            self.item_prices = [initial_item0_price, initial_item1_price]

        # Moonshot
        self.moonshot = moonshot
        if self.moonshot:
            self.moonshot_threshold = moonshot_threshold
            self.moonshot_percent = moonshot_percent

    def set_item_prices(self):
        if self.project_part == 1:
            self.item_prices = self.current_covariates
        elif self.optimizer:
            prices, rev = self.optimizer.get_revenue_maximizing_prices_and_revenue_from_cov(self.current_covariates)
            self.item_prices = prices

    # This is where we take in any information regarding what has happened and store it
    def process_last_sale(self, obs):
        # Update General Params
        self.round_number += 1
        new_buyer_covariates, last_sale, state = obs
        self.current_covariates = new_buyer_covariates
        # Current Profits for each Agent
        self.profit = state[self.this_agent_number]
        self.op_profit = state[self.op_number]
        # Last round prices offered
        self.last_prices = last_sale[2][self.this_agent_number]
        self.op_last_prices = last_sale[2][self.op_number]
        # Details of the last sale
        self.did_customer_buy_from_me = last_sale[1] == self.this_agent_number
        self.item_bought = last_sale[0]

        # Determine last op alpha
        alpha = 1
        if self.round_number > 1:
            if self.single_alpha:
                max_discount = 0
                for i in range(self.n_items):
                    discount = self.last_cust_values[i] - self.op_last_prices[i]
                    if discount > max_discount:
                        alpha = min(self.op_last_prices[i] / max(self.last_cust_values[i], 0.01), 1)
                self.last_op_alphas = [alpha for _ in range(self.n_items)]
            else:
                self.last_op_alphas = [min(self.op_last_prices[i] / max(self.last_cust_values[i], 0.01), 1)
                                       for i in range(self.n_items)]

    # This is where we will update alpha and any other attributes which will lead to what our price decision is
    def update_decision(self):
        self.set_item_prices()

    def bound_alpha(self):
        for i in range(self.n_items):
            if self.alphas[i] > self.upper_alpha_threshold:
                self.alphas[i] = self.upper_alpha_reset
            elif self.alphas[i] < self.lower_alpha_threshold:
                self.alphas[i] = self.lower_alpha_reset

    def update_cust_values(self):
        if self.project_part == 1:
            self.last_cust_values = self.current_covariates
        else:
            self.last_cust_values = self.item_prices

    def pre_action(self, obs):
        self.process_last_sale(obs)
        self.update_decision()
        self.bound_alpha()
        self.update_cust_values()

    # This is what is called by the env and where we must encapsulate logic to call other functions and submit the
    # price at which we want to charge.
    def action(self, obs):
        # Update params and process last sale
        self.pre_action(obs)
        action = []
        for i in range(self.n_items):
            if self.moonshot and (np.random.rand() < self.moonshot_percent and self.item_prices[i] < self.moonshot_threshold):
                action.append(sys.maxsize)
            else:
                action.append(self.item_prices[i] * self.alphas[i] - 0.0001)
        return action
