import sys
from os import path
from random import getrandbits, choice
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from HitlerPlayer import HitlerPlayer, Ja, Nein
import operator
name = "SecretHitler"

class SecretHitler(HitlerPlayer):
    def __init__(self, id, name, role, state):
        super(SecretHitler, self).__init__(id, name, role, state)

    # Hlasovani o vlade
    def vote(self):
        """
        Always vote yes to a vote involving at least one fascist if you're fascist, randomly otherwise
        """
        if self.state.president in self.fascists or self.state.chancellor in self.fascists:
            return Ja()
        else:
            return Nein()

    def nominate_chancellor(self):
        if self.is_fascist and not self.is_hitler and self.state.ex_president != self.hitler and self.state.chancellor != self.hitler:
            return self.hitler
        assert len(self.state.players) > 0
        chancellor = self
        while chancellor == self:
            chancellor = choice(self.state.players)
        return chancellor

    def view_policies(self, policies):
        pass

    @property
    def kill(self):
        kill = self
        while kill == self or kill.is_dead or (self.is_fascist and len(self.fascists) > 0 and kill in self.fascists):
            kill = choice(self.state.players)
        return kill

    def inspect_player(self):
        inspect = self
        while inspect == self or inspect.is_dead:
            inspect = choice(self.state.players)
        return inspect

    def choose_next(self):
        choose = self
        while choose == self or choose.is_hitler or choose.is_dead or (
                self.is_fascist and len(self.fascists) > 0 and choose not in self.fascists):
            choose = choice(self.state.players)
        return choose

    def enact_policy(self, policies):
        if policies[0].type == "liberal":
            return policies[0], policies[1]
        return policies[1], policies[0]

    def filter_policies(self, policies):
        choices = []
        for policy in policies:
            if self.state.fascist_track >= 3 and policy.type == "fascist" and len(choices) < 2:
                choices += [policy]
            elif policy.type == "liberal" and len(choices) < 2:
                choices += [policy]

        while len(choices) < 2:
            choices += [list(filter(lambda x: x not in choices, policies))[0]]
        return choices, list(filter(lambda x: x not in choices, policies))[0]

    def veto(self, policies):
        return False


    # Nastaveni hodnoceni na zacatku hry.
    def evaluate(self):
        pass

    # Zmeny hodnoceni
    def reevaluate(self, player1_id, player2_id, policy):
        pass
