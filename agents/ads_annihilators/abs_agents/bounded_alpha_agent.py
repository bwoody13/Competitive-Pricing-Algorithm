from agents import load

AlphaAgent = load('ads-annihilators/abs_agents/alpha_agent.py').AlphaAgent
# While this is not valid to use for importing when called during competition, it will help when coding in your IDE
# since this way you can do proper type checking and autofill. Make sure to comment before commits / pushes.
# from alpha_agent import AlphaAgent


class BoundedAlphaAgent(AlphaAgent):
    def __init__(self, *args,
                 upper_alpha_threshold=1.0,
                 upper_alpha_reset=0.99,
                 lower_alpha_threshold=0.0,
                 lower_alpha_reset=0.1,
                 **kwargs):
        super().__init__(*args, **kwargs)
        # Bounds that put alpha within a specific range
        self.upper_alpha_threshold = upper_alpha_threshold
        self.upper_alpha_reset = upper_alpha_reset
        self.lower_alpha_threshold = lower_alpha_threshold
        self.lower_alpha_reset = lower_alpha_reset

    def update_decision(self):
        super().update_decision()

        if self.alpha > self.upper_alpha_threshold:
            self.alpha = self.upper_alpha_reset
        elif self.alpha < self.lower_alpha_threshold:
            self.alpha = self.lower_alpha_reset
