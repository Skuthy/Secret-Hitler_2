import sys
from os import path
from random import getrandbits, choice
from HitlerBoard import HitlerState
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from HitlerPlayer import HitlerPlayer, Ja, Nein

name = "GoodGuy"


class GoodGuy(HitlerPlayer):
    def __init__(self, id, name, role, state):
        super(GoodGuy, self).__init__(id, name, role, state)

    def vote(self):
        if self.state.president == self or self.state.chancellor == self or self.state.failed_votes == 2:
            return Ja()
        else:
            return Nein()

    def nominate_chancellor(self):
        """
        More random!
        :return: HitlerPlayer
        """
        assert len(self.state.players) > 0
        chancellor = self
        while chancellor == self:
            chancellor = choice(self.state.players)
        # print("Player #%d choosing chancellor: %s" % (self.id, chancellor.id))
        return chancellor

    def view_policies(self, policies):
        """
        What to do if you perform the presidential action to view the top three policies
        :return:
        """
        pass

    @property
    def kill(self):
        """
        Choose a person to kill
        :return:
        """
        # self.inspected_player
        try:
            for k, v in self.inspected_players.items():
                if v == "fascist" and not k.is_dead:
                    kill = k
                    return kill
        except:
            print("chyba zabijeni")
        kill = self
        while kill == self or kill.is_dead or kill == self.state.chancellor:
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
        Choose the next president
        :return:
        """
        choose = self
        while choose == self or choose.is_dead:
            choose = choice(self.state.players)
        return choose

    def enact_policy(self, policies):
        if policies[0].type == "liberal":
            return policies[0], policies[1]
        return policies[1], policies[0]

    def filter_policies(self, policies):
        choices = []
        for policy in policies:
            if policy.type == "liberal" and len(choices) < 2:
                choices += [policy]

        while len(choices) < 2:
            choices += [list(filter(lambda x: x not in choices, policies))[0]]
        return choices, list(filter(lambda x: x not in choices, policies))[0]

    def veto(self, policies):
        if policies.type == "fascist":
            return True
        return False

    def reevaluate(self, player1, player2, policy):
        pass

    def evaluate(self):
        pass
