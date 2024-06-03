# Competitive Pricing Algorithm

This project consisted of many different aspects that contributed to a final pricing algorithm.

Firstly, game theory was applied to consider how opponents may behave and react to our own pricing decisions. This led to a combination of cooperation, exploitation, and predicting opponent behavior. We also added safeguards to estimated predictions of opponents so that we never priced too low or too high.

To aid in competing against different opponents, we added A/B testing which allowed us to tune and test certain hyperparameters of our agent during a match and optimize against specific opponents. We also created internal simulations that allowed us to do round-robin tournaments or specific head-to-head matches that ran a large number of times highlihgting the overall performance and aggregating statistics.

To determine the optimal prices to charge, we needed a way to estimate the best prices given the customer covariates. An XGBoost model was trained on historical data to estimate demand. Using the demand estimations, a price grid was traversed to determine the price which would yield the highest revenue. Using this information, we feed this into our agent which will then adjust the price according to the current competitive landscape.

In the end, the combination of our strategic approaches led us to take first place in the competition against 20 teams.
