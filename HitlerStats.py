from HitlerPlayer import HitlerPlayer

class HitlerStats():
    def __init__(self):
        self.random_policies_played = 0
        self.agent_wins = {}

    def rando(self):
        self.random_policies_played += 1
    
    def add_agent_win(self, id):
        if id not in self.agent_wins.keys():
            self.agent_wins[id] = 0
        self.agent_wins[id] += 1
        