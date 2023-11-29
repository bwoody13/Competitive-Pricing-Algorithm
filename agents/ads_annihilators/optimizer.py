import numpy as np
import pickle


class Optimizer:
    def __init__(self,
                 model_file="agents/ads_annihilators/xgbclassifier_v1.pkl",
                 bought_range_p0=15,
                 # over_range1_p0=4,
                 # over_range2_p0=3,
                 bought_range_p1=20,
                 # over_range1_p1=4,
                 # over_range2_p1=3,
                 ):
        self.model = pickle.load(open(model_file, 'rb'))

        # The following mins and maxes are from analysis of training data
        # and found in the optimize revenue notebook (note these are slightly rounded)
        self.min_p0 = 0.01  # 3.3
        self.min_p1 = 0.01
        self.max_p0_b = 90
        self.max_p1_b = 133.45
        self.max_p0 = 373
        self.max_p1 = 548

        # The ranges to use within the linspace for p0 and p1 prices to offer
        self.bought_range_p0 = bought_range_p0
        # self.over_range1_p0 = over_range1_p0
        # self.over_range2_p0 = over_range2_p0
        self.bought_range_p1 = bought_range_p1
        # self.over_range1_p1 = over_range1_p1
        # self.over_range2_p1 = over_range2_p1

        # Make price combinations based on range of prices
        self.price_combinations = self._make_prices_to_predict()

    def _make_prices_to_predict(self):
        '''
        Make range of prices to check for optimality. We want there to be more options
        in which there were items bought and consider fewer of the prices where there
        was no purchase for that item.
        :return: combination of all price pairs for item0 and item1
        '''
        # p0_to_predict_comb = np.concatenate([
        #     np.linspace(self.min_p0, self.max_p0_b, self.bought_range_p0),
        #     np.linspace(self.max_p0_b + 0.1, self.max_p0 / 3, self.over_range1_p0),
        #     np.linspace(self.max_p0 / 3 + 0.1, self.max_p0, self.over_range2_p0)
        # ])
        # p1_to_predict_comb = np.concatenate([
        #     np.linspace(self.min_p1, self.max_p1_b, self.bought_range_p1),
        #     np.linspace(self.max_p1_b + 0.1, self.max_p1 / 3, self.over_range1_p1),
        #     np.linspace(self.max_p0 / 3 + 0.1, self.max_p1, self.over_range2_p1)
        # ])
        p0_to_predict_comb = np.linspace(self.min_p0, self.max_p0_b, self.bought_range_p0)
        p1_to_predict_comb = np.linspace(self.min_p1, self.max_p1_b, self.bought_range_p1)

        p0_grid, p1_grid = np.meshgrid(p0_to_predict_comb, p1_to_predict_comb)
        return np.column_stack([p0_grid.ravel(), p1_grid.ravel()])

    def get_demand_at_prices(self, covs):
        covs_repeated = np.repeat([covs], len(self.price_combinations), axis=0)
        X = np.hstack([covs_repeated, self.price_combinations])
        return self.model.predict_proba(X)[:, 0:-1]     # omit prob don't buy

    def get_revenue_maximizing_prices_and_revenue(self, demand):
        max_revenue = 0
        max_prices = (0, 0)

        for price_pair, demand in zip(self.price_combinations, demand):
            p0, p1 = price_pair
            demand0, demand1 = demand

            revenue = p0 * demand0 + p1 * demand1

            if revenue > max_revenue:
                max_revenue = revenue
                max_prices = (p0, p1)

        return max_prices, max_revenue

    def get_revenue_maximizing_prices_and_revenue_from_cov(self, covs):
        return self.get_revenue_maximizing_prices_and_revenue(self.get_demand_at_prices(covs))
