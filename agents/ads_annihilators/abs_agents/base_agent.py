# This is the base level agent behaviour which every agent is a subclass of.
class BaseAgent(object):
    def __init__(self, agent_number, params={}, **kwargs):
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


    # This is where we take in any information regarding what has happened and store it
    def process_last_sale(self, obs):
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

    # This is where we will update alpha and any other attributes which will lead to what our price decision is
    def update_decision(self):
        pass

    # This is what is called by the env and where we must encapsulate logic to call other functions and submit the
    # price at which we want to charge. This needs to be implmenented by subclasses.
    def action(self, obs):
        raise NotImplementedError("To Be Implemented by Subclass")
