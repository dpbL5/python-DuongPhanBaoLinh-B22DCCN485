class Player:
    # constructor
    def __init__(self, stats_set: set):
        self.stats = dict()
        # initialize all stats to 'N/a'
        for key in stats_set:
            self.stats[key] = 'N/a'