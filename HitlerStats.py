from HitlerPlayer import HitlerPlayer

class HitlerStats():
    def __init__(self):
        # pocet failnutych votu
        self.random_policies_played = 0
        self.agent_wins = {}
        self.agent_kills = {}

    def rando(self):
        self.random_policies_played += 1

    def add_agent_win(self, name):
        if name not in self.agent_wins.keys():
            self.agent_wins[name] = 0
        self.agent_wins[name] += 1

    def smrti(self, name):
        if name not in self.agent_kills.keys():
            self.agent_kills[name] = 0
        self.agent_kills[name] += 1