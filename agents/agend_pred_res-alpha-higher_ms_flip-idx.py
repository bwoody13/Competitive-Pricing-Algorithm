from agents.ads_annihilators.abs_agents.base_predictive_ms import BasePredictiveMS


class Agent(BasePredictiveMS):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, lower_alpha_reset=0.4, **kwargs)
        self.true_agent.this_agent_number = self.op_number
        self.true_agent.op_number = self.this_agent_number