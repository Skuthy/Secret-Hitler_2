import sys
from os import path
from random import getrandbits, choice

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from HitlerPlayer import HitlerPlayer, Ja, Nein

name = "DumbOvertFascist"


class DumbOvertFascist(HitlerPlayer):
    def __init_(self, id, name, role, state):
        super(DumbOvertFascist, self).__init__(id, name, role, state)

    def vote(self):
        """
        Always vote yes to a vote involving at least one fascist if you're fascist, randomly otherwise
        """
        if self.is_fascist and len(self.fascists) > 0:
            if self.state.president in self.fascists or self.state.chancellor in self.fascists:
                return Ja()
            else:
                return Nein()
        if bool(getrandbits(1)):
            return Ja()
        else:
            return Nein()

    def nominate_chancellor(self):
        """
        Nominate Hitler as chancellor if fascist, randomly otherwise
        """
        if self.is_fascist and not self.is_hitler and self.state.ex_president != self.hitler and self.state.chancellor != self.hitler:
            return self.hitler
        assert len(self.state.players) > 0
        chancellor = self
        while chancellor == self:
            chancellor = choice(self.state.players)
        return chancellor

    def view_policies(self, policies):
        """
        What to do if you perform the presidential action to view the top three policies
        :return:
        """
        pass

    def kill(self):
        """
        Choose a person to kill
        :return:
        """
        kill = self
        while kill == self or kill.is_dead or (self.is_fascist and len(self.fascists) > 0 and kill in self.fascists):
            kill = choice(self.state.players)
        return kill

    def inspect_player(self):
        """
        Choose a person's party membership to inspect
        :return:
        """
        inspect = self
        while inspect == self or inspect.is_dead:
            inspect = choice(self.state.players)
        return inspect

    def choose_next(self):
        """
        Choose the next president - always fascist if fascist!
        :return:
        """
        choose = self
        while choose == self or choose.is_dead or (
                self.is_fascist and len(self.fascists) > 0 and choose not in self.fascists):
            choose = choice(self.state.players)
        return choose

    def enact_policy(self, policies):
        if self.is_fascist:
            if policies[0].type == "fascist":
                return policies[0], policies[1]
            else:
                return policies[1], policies[0]
        if policies[0].type == "liberal":
            return policies[0], policies[1]
        return policies[1], policies[0]

    def filter_policies(self, policies):
        """
        if fascist, bury a liberal if you can.
        """
        choices = []
        if self.is_fascist:
            for policy in policies:
                if policy.type == "fascist" and len(choices) < 2:
                    choices += [policy]
        else:
            for policy in policies:
                if policy.type == "liberal" and len(choices) < 2:
                    choices += [policy]

        while len(choices) < 2:
            choices += [list(filter(lambda x: x not in choices, policies))[0]]
        return choices, list(filter(lambda x: x not in choices, policies))[0]

    def veto(self, policies):
        if self.is_fascist:
            return False
        else:
            return True
