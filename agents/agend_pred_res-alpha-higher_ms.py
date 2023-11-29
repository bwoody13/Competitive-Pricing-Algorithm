from agents.ads_annihilators.abs_agents.base_predictive_ms import BasePredictiveMS


class Agent(BasePredictiveMS):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, lower_alpha_threshold=0.2, lower_alpha_reset=0.5, **kwargs)
