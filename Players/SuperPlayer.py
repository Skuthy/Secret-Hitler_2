import sys
from os import path
from random import getrandbits, choice
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from HitlerPlayer import HitlerPlayer, Ja, Nein
import operator
name = "SuperPlayer"

class SuperPlayer(HitlerPlayer):
    def __init__(self, id, name, role, state):
        super(SuperPlayer, self).__init__(id, name, role, state)
        self.evaluation_players = {}

    def vote(self):
        if self.state.fascist_track >= 3 and (self.evaluation_players[self.state.president.id] < 40 and self.evaluation_players[self.state.chancellor.id] < 40):
            return Nein()
        if ((self.state.president == self and self.evaluation_players[self.state.chancellor.id] >= 50)\
            or (self.state.chancellor == self and self.evaluation_players[self.state.president.id] >= 40)\
                or (self.state.failed_votes == 2) or (self.evaluation_players[self.state.president.id] >= 50 and self.evaluation_players[self.state.chancellor.id] >= 50)):
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
        sorted_dict = {k: v for k, v in sorted(self.evaluation_players.items(), key=lambda item: item[1], reverse=True)}
        for i in sorted_dict.keys():
            chancellor = self.state.players[i]
            if chancellor is not self and not chancellor.is_dead and chancellor is not self.state.chancellor and chancellor is not self.state.ex_president:
                break
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
        # self.inspected_player
        try:
            for k, v in self.inspected_players.items():
                if v == "fascist" and not k.is_dead:
                    kill = k
                    return kill
        except:
            print("chyba zabijeni")

        kill = self

        sorted_dict = {k: v for k, v in sorted(self.evaluation_players.items(), key=lambda item: item[1])}
        for i in sorted_dict.keys():
            kill = self.state.players[i]
            if kill is not self and not kill.is_dead and kill is not self.state.chancellor:
                break
        return kill

    def inspect_player(self):
        """
        Choose a person's party membership to inspect
        :return:
        """
        inspect = self
        while inspect == self or inspect.is_dead:
            inspect = choice(self.state.players)

        if inspect.role.party_membership == "liberal":
            self.evaluation_players[inspect.id] = 100
        else:
            self.evaluation_players[inspect.id] = self.evaluation_players[inspect.id] - 100

    #print("Player #%d inspecting: %s" % (self.id, inspect.id))
        return inspect

    def choose_next(self):
        """
        Choose the next president
        :return:
        """
        choose = self
        sorted_dict = {k: v for k, v in sorted(self.evaluation_players.items(), key=lambda item: item[1], reverse=True)}
        for i in sorted_dict.keys():
            choose = self.state.players[i]
            if choose is not self and not choose.is_dead:
                break
        #print("Player #%d choosing: %s" % (self.id, choose.id))
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

    def evaluate(self):
        for i in self.state.players:
            if self.id == i.id:
                self.evaluation_players[i.id] = 100
            else:
                self.evaluation_players[i.id] = 50

    def reevaluate(self, player1_id, player2_id, policy):
        if self.id is not player1_id:
            if policy =="liberal":
                self.evaluation_players[player1_id] = self.evaluation_players[player1_id] + 10
            else:
                self.evaluation_players[player1_id] = self.evaluation_players[player1_id] - 10
        if self.id is not player2_id:
            if policy == "liberal":
                self.evaluation_players[player1_id] = self.evaluation_players[player1_id] + 10
            else:
                self.evaluation_players[player2_id] = self.evaluation_players[player2_id] - 10
