from agents.ads_annihilators.abs_agents.base_predictive import BasePredictive
from agents.ads_annihilators.abs_agents.moonshot import Moonshot


class BasePredictiveMS(Moonshot):
    def __init__(self, *args, **kwargs):
        true_agent = BasePredictive(*args, **kwargs)
        super().__init__(*args, true_agent=true_agent, **kwargs)

