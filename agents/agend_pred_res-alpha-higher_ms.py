from agents.ads_annihilators.abs_agents.base_predictive_ms import BasePredictiveMS


class Agent(BasePredictiveMS):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, lower_alpha_reset=0.4, **kwargs)
