import sys
from os import path
from random import getrandbits, choice
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from HitlerPlayer import HitlerPlayer, Ja, Nein

name = "SelfishRandom"

class SelfishRandom(HitlerPlayer):
    def __init__(self, id, name, role, state):
        super(SelfishRandom, self).__init__(id, name, role, state)

    def vote(self):
        """
        Just do it randomly :D
        :return: Random Ja or Nein
        """
        if bool(getrandbits(1)):
            #print("Player #%d voting Ja" % self.id)
            return Ja()
        else:
            #print("Player #%d voting Nein" % self.id)
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
        #print("Player #%d killing: %s" % (self.id, kill.id))
        return kill

    def inspect_player(self):
        """
        Choose a person's party membership to inspect
        :return:
        """
        inspect = self
        while inspect == self or inspect.is_dead:
            inspect = choice(self.state.players)
        #print("Player #%d inspecting: %s" % (self.id, inspect.id))
        return inspect

    def choose_next(self):
        """
        Choose the next president
        :return:
        """
        choose = self
        while choose == self or choose.is_dead:
            choose = choice(self.state.players)
        #print("Player #%d choosing: %s" % (self.id, choose.id))
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
        veto = bool(getrandbits(1))
        #print("Player #%d choosing to veto: %s" % (self.id, veto))
        return veto

    def reevaluate(self, player1, player2, policy):
        pass

    def evaluate(self):
        pass