import sys
from os import path
from random import getrandbits, choice
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from HitlerPlayer import HitlerPlayer, Ja, Nein

name = "TrustingPlayer"

class TrustingPlayer(HitlerPlayer):
    def __init__(self, id, name, role, state):
        super(TrustingPlayer, self).__init__(id, name, role, state)

    def vote(self):
        """
        Always vote Ja!
        """
        return Ja()

    def nominate_chancellor(self):
        """
        More random!
        :return: HitlerPlayer
        """
        assert len(self.state.players) > 0
        chancellor = self
        while chancellor == self:
            chancellor = choice(self.state.players)
        #print("Player #%d choosing chancellor: %s" % (self.id, chancellor.id))
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
        kill = self
        while kill == self or kill.is_dead:
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
        return (policies[0], policies[1])

    def filter_policies(self, policies):
        return ([policies[0], policies[1]], policies[2])

    def veto(self, policies):
        return False

    def evaluate(self, player1, player2, policy):
        pass