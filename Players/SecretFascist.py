import sys
from os import path
from random import getrandbits, choice
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from HitlerPlayer import HitlerPlayer, Ja, Nein
import operator
name = "SecretFascist"

# Nevyzpytatelný Fašista
class SecretFascist(HitlerPlayer):
    def __init__(self, id, name, role, state):
        super(SecretFascist, self).__init__(id, name, role, state)

    # Hlasovani o vlade, voli zase jen pro fašisty
    def vote(self):
        """
        Always vote yes to a vote involving at least one fascist if you're fascist, randomly otherwise
        """
        if self.state.president in self.fascists or self.state.chancellor in self.fascists:
            return Ja()
        else:
            return Nein()

    # vol si k sobe Hitlera pokud to znamena vyhru, jinak nahodne
    def nominate_chancellor(self):
        if self.is_fascist and not self.is_hitler and self.state.ex_president != self.hitler and self.state.chancellor != self.hitler and self.state.fascist_track >= 3:
            return self.hitler
        assert len(self.state.players) > 0
        chancellor = self
        while chancellor == self:
            chancellor = choice(self.state.players)
        return chancellor

    def view_policies(self, policies):
        pass

    # zabij nekoho kdo neni fasista
    @property
    def kill(self):
        kill = self
        while kill == self or kill.is_dead or (self.is_fascist and len(self.fascists) > 0 and kill in self.fascists):
            kill = choice(self.state.players)
        return kill

    # random inspect
    def inspect_player(self):
        inspect = self
        while inspect == self or inspect.is_dead:
            inspect = choice(self.state.players)
        return inspect

    # vyber dalsiho Prezidenta, nechceme Hitlera, protože toho potřebujeme na funkci Kancléře
    def choose_next(self):
        choose = self
        while choose == self or choose.is_dead or choose.is_hitler or (
                self.is_fascist and len(self.fascists) > 0 and choose not in self.fascists):
            choose = choice(self.state.players)
        return choose

    # pokud si Hitler vykládej liberalni zakony, jako fasista fasisticke
    def enact_policy(self, policies):
        if self.is_hitler:
            if policies[0].type == "liberal":
                return policies[0], policies[1]
            return policies[1], policies[0]
        else:
            if policies[0].type == "fascist":
                return policies[0], policies[1]
            return policies[1], policies[0]

    # Hitler bude ze zacatku posilat liberalni zakony, aby mel lepsi hodnoceni, pote fasisticke. Fasiste se porad budou snazit posilat fasisticke zakony
    def filter_policies(self, policies):
        choices = []
        for policy in policies:
            if self.is_hitler and self.state.fascist_track >= 3 and policy.type == "fascist" and len(choices) < 2:
                choices += [policy]
            else:
                if self.is_hitler and policy.type == "liberal" and len(choices) < 2:
                    choices += [policy]
                elif policy.type == "fascist" and len(choices) < 2:
                    choices += [policy]

        while len(choices) < 2:
            choices += [list(filter(lambda x: x not in choices, policies))[0]]
        return choices, list(filter(lambda x: x not in choices, policies))[0]

    # jestli muzou vylozit fasistickou kartu tak veto nechceme, jinak ano
    def veto(self, policies):
        if policies.type == "fascist":
            return False
        return True


    # Nastaveni hodnoceni na zacatku hry.
    def evaluate(self):
        pass

    # Zmeny hodnoceni
    def reevaluate(self, player1_id, player2_id, policy):
        pass
