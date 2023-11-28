from agents.ads_annihilators.abs_agents.base_coop_exploit import BaseCoopExploit


class BasePredictive(BaseCoopExploit):
    def __init__(self, *args, future_reward_multiplier=40, **kwargs):
        super().__init__(*args, **kwargs)
        # Predictive Alphas
        self.pred_op_alpha1 = [1.0 for _ in range(self.n_items)]
        self.pred_op_alpha2 = [1.0 for _ in range(self.n_items)]
        self.pred_op_alpha3 = [1.0 for _ in range(self.n_items)]
        self.pred_op_alpha4 = [1.0 for _ in range(self.n_items)]

        # Reward and Action
        self.future_reward_multiplier = future_reward_multiplier
        self.top_reward = 0
        self.top_actions = [[1, 1, 1, 1] for _ in range(self.n_items)]

    def tree_search(self, i):
        self.top_reward = 0
        base_alphas = [0, 1, self.base_normalization + self.ema_weight * self.op_alpha_emas[i]]
        for action1 in base_alphas:
            self.pred_op_alpha2 = self.predict_ts([action1])
            possible_alphas2 = (
                    base_alphas + [self.pred_op_alpha2[i] * 0.99])

            for action2 in possible_alphas2:
                self.pred_op_alpha3 = self.predict_ts([action1, action2])
                possible_alphas3 = base_alphas + [self.pred_op_alpha3[i] * 0.99]

                for action3 in possible_alphas3:
                    self.pred_op_alpha4 = self.predict_ts([action1, action2, action3])
                    possible_alphas4 = base_alphas + [self.pred_op_alpha4[i] * 0.99]

                    for action4 in possible_alphas4:
                        self.evaluate_reward(action1, action2, action3, action4, i)

    def predict_ts(self, actions=None):
        if actions is not None:
            for action in actions:
                for i in range(self.n_items):
                    if action > self.pred_op_alphas[i]:
                        self.pred_op_alphas[i] = min(1.1 * self.pred_op_alphas[i], 1)
                    else:
                        self.pred_op_alphas[i] *= .9

        self.op_alpha_emas = [0.8 * self.op_alpha_emas[i] + 0.2 * self.pred_op_alphas[i] for i in range(self.n_items)]
        prediction = self.op_alpha_emas
        return prediction

    def evaluate_reward(self, action1, action2, action3, action4, i):
        self.pred_reward = 0
        pred_op_alphas = [self.pred_op_alpha1[i], self.pred_op_alpha2[i], self.pred_op_alpha3[i], self.pred_op_alpha4[i]]

        for action, pred_op_alpha in zip([action1, action2, action3, action4], pred_op_alphas):
            if action < pred_op_alpha:
                self.pred_reward += action

        self.pred_reward += self.pred_op_alpha4[i] * self.future_reward_multiplier

        if self.pred_reward > self.top_reward:
            self.top_reward = self.pred_reward
            self.top_actions[i] = [action1, action2, action3, action4]

    # Override
    def baseline(self, i):
        if self.round_number > 1:
            self.tree_search(i)
            self.alphas[i] = self.top_actions[i][0]