class Agent(BaseCoopExploit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                         single_alpha=True,
                         exploit_threshold=75,
                         **kwargs)
