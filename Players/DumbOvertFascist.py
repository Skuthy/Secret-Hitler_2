import sys
from os import path
from random import getrandbits, choice

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from HitlerPlayer import HitlerPlayer, Ja, Nein

name = "DumbOvertFascist"

# Hloupý Fašista
# chová se se vším všudy jako Fašista, vykládá pouze Fašistické politiky, volí jen pro Fašisty, zabíjí Liberály...
class DumbOvertFascist(HitlerPlayer):
    def __init_(self, id, name, role, state):
        super(DumbOvertFascist, self).__init__(id, name, role, state)
# pokud je ve vládě Fašista vol Ja
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
# ber si k sobě vždy Hitlera pokud můžeš, jinak random
    def nominate_chancellor(self):
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
    # zabij nekoho kdo neni fasista
    @property
    def kill(self):
        kill = self
        while kill == self or kill.is_dead or (self.is_fascist and len(self.fascists) > 0 and kill in self.fascists):
            kill = choice(self.state.players)
        return kill
# koukni na náhodného hráče (je mu to už jedno, zná role všech)
    def inspect_player(self):
        inspect = self
        while inspect == self or inspect.is_dead:
            inspect = choice(self.state.players)
        return inspect
# vyber dálšího fašistického Prezidenta
    def choose_next(self):
        choose = self
        while choose == self or choose.is_hitler or choose.is_dead or (
                self.is_fascist and len(self.fascists) > 0 and choose not in self.fascists):
            choose = choice(self.state.players)
        return choose
# vylož fašistickou politiku
    def enact_policy(self, policies):
        if self.is_fascist:
            if policies[0].type == "fascist":
                return policies[0], policies[1]
            else:
                return policies[1], policies[0]
        if policies[0].type == "liberal":
            return policies[0], policies[1]
        return policies[1], policies[0]
# pošli fašistické politiky
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
# nechce vetovat
    def veto(self, policies):
        if self.is_fascist:
            return False
        else:
            return True
    def reevaluate(self, player1, player2, policy):
        pass

    def evaluate(self):
        pass