class Scoreboard:
    def __init__(self):
        self.scores = {}
    def set_score(self, player, score):
        self.scores[player] = score
    def get_score(self, player):
        return self.scores.get(player, 0)
    def reset(self):
        self.scores = {}
