from typing import List, Any

from HitlerBoard import HitlerBoard, HitlerState
from HitlerStats import HitlerStats
from random import randint, choice
from tqdm import tqdm
import importlib
import Players
from Players.DumbOvertFascist import DumbOvertFascist
from Players.DumbPlayer import DumbPlayer
from Players.GoodGuy import GoodGuy
from Players.TrustingPlayer import TrustingPlayer



class HitlerGame(object):
    def __init__(self, playernum=0, stats=None):
        """Stuff"""
        self.HitlerState = None
        self.playernum = playernum
        self.hitler = None
        self.board = None
        self.state = HitlerState()
        self.stats = stats
        self.playertypes = []

    def play(self):
        """Main game loop"""
        self.load_players()
        self.assign_players()
        self.inform_fascists()
        self.choose_first_president()

        loop_game = True

        while loop_game:
            # print("turn")
            loop_game = not self.turn()

        # print("Game's over!")
        return self.finish_game()

    def turn(self):
        """
        Take a turn.
        return: boolean - true if game finished, false if continue playing
        """
        # First, pass on the presidency
        self.set_next_president()

        # Ask the president to nominate a chancellor
        self.state.chancellor = self.nominate_chancellor()

        # Ask the players to vote whether they want this pairing
        voted = self.voting()

        if not voted:
            # print("Vote failed!")
            action_enacted = self.vote_failed()
        else:
            # Possibility to win if Hitler is chancellor and more than 2 fascist policies enacted.
            if self.hitler_chancellor_win():
                return True

            action_enacted = self.vote_passed()

        if action_enacted:
            self.perform_vote_action()

        if self.policy_win():
            return True

        if self.hitler.is_dead:
            return True

        return False

    def load_players(self):
        for player in Players.__all__:
            name = getattr(importlib.import_module("Players." + player), "name")
            self.playertypes.append(getattr(importlib.import_module("Players." + player), name))

    def assign_players(self):
        if self.playernum == 0:
            self.playernum = int(input("How many players?\n"))

        self.board = HitlerBoard(self.state, self.playernum)
        roles = self.board.shuffle_roles()
        pocet = 0
        for num in range(self.playernum):
            # name = raw_input("Player #%d's name?\n" % num)
            #if str(roles[0]) == 'liberal':
            if str(roles[0]) == 'liberal' and pocet == 0:
                playertype = GoodGuy #choice(self.playertypes)
                pocet = pocet + 1
            else:
                # print(roles)
                playertype = DumbPlayer
            #playertype = TrustingPlayer DumbOvertFascist DumbPlayer
            name = playertype.__name__ + ": " + str(num)
            player = playertype(num,
                                name,
                                roles.pop(0),
                                self.state)

            if player.is_hitler:
                # Keep track of Hitler
                self.hitler = player

            self.state.players.append(player)

    def inform_fascists(self):
        """
        Inform the fascists who the other fascists are.
        If there are 5 or 6 players, Hitler knows who the other fascist is.
        """
        fascists = [player for player in self.state.players if player.is_fascist]

        for fascist in fascists:
            # Every fascist knows who Hitler is
            fascist.hitler = self.hitler
            if self.playernum in [5, 6]:
                # Hitler knows about the other fascist
                fascist.fascists = fascists
            elif not fascist.is_hitler:
                # Hitler doesn't know about the other fascists
                fascist.fascists = fascists

    def choose_first_president(self):
        """
        Choose a random player to be the 'zeroth' president, the first president will
        be the next person after them.
        """
        self.state.president = self.state.players[randint(0, len(self.state.players) - 1)]

    def set_next_president(self):
        self.state.president = self.state.players[(self.state.president.id + 1) % len(self.state.players)]
        if self.state.president.is_dead:
            self.set_next_president()

    def nominate_chancellor(self):
        chancellor = self.state.chancellor
        while (chancellor == self.state.chancellor or
               chancellor == self.state.president or
               (self.playernum in [5, 6] and
                chancellor == self.state.ex_president) or
               chancellor.is_dead):
            chancellor = self.state.president.nominate_chancellor()
        # nutna kontrola v nominate_chancellor pro kazdeho hrace - aby volil validniho chancellora nebo se to zacykli
        return chancellor

    def voting(self):
        """
        Get votes for the current pairing from all players.
        :returns: Whether the vote succeeded
        """
        self.state.last_votes = []
        for player in self.state.players:
            if not player.is_dead:
                self.state.last_votes.append(player.vote())

        positivity = 0

        for vote in self.state.last_votes:
            # votes are booleans - if vote means if vote == true
            if vote:
                positivity += 1
            else:
                positivity -= 1

        return positivity > 0

    def vote_failed(self):
        self.state.failed_votes += 1

        if self.state.failed_votes == 3:
            self.state.failed_votes = 0
            self.stats.rando()
            # print("Too many failed votes! Citizens are taking action into their own hands")
            return self.board.enact_policy(self.board.draw_policy(1)[0])

        else:
            # Not enacting a vote, take another turn
            return False

    def vote_passed(self):
        """
        The vote has passed! Get the president and chancellor to do their thang.
        """
        # print("Vote passed!")
        self.state.failed_votes = 0

        (take, discard) = self.state.president.filter_policies(self.board.draw_policy(3))
        self.board.discards.append(discard)

        if (self.state.veto and
                self.state.chancellor.veto(take) and
                self.state.president.veto(take)):
            self.board.discards = take + self.board.discards
            return self.vote_failed()

        (enact, discard) = self.state.chancellor.enact_policy(take)
        self.board.discards.append(discard)
        return self.board.enact_policy(enact)

    def hitler_chancellor_win(self):
        return (self.state.fascist_track >= 3 and
                self.state.chancellor == self.hitler)

    def policy_win(self):
        return self.state.liberal_track == 5 or self.state.fascist_track == 6

    def perform_vote_action(self):
        action = self.board.fascist_track_actions[self.state.fascist_track - 1]

        if action is None:
            #print("No action")
            return

        #print("Performing vote action: %s" % action)

        if action == "policy":
            top_three = self.board.draw_policy(3)
            self.state.president.view_policies(top_three)
            self.board.return_policy(top_three)

        elif action == "kill":
            killed_player = self.state.president.kill
            while killed_player.is_dead or killed_player == self.state.president:
                killed_player = self.state.president.kill
            killed_player.is_dead = True

            if killed_player.is_fascist and not killed_player.is_hitler:
                self.stats.smrti('Fascist kills')
            elif killed_player.is_fascist:
                self.stats.smrti('Hitler kills')
            else:
                self.stats.smrti('Liberal kills')
        elif action == "inspect":
            inspected_player = self.state.president
            while inspected_player.is_dead or inspected_player == self.state.president:
                inspected_player = self.state.president.inspect_player()
                self.state.president.inspected_players[inspected_player] = inspected_player.role.party_membership
        elif action == "choose":
            chosen = self.state.president
            while chosen == self.state.president or chosen.is_dead:
                chosen = self.state.president.choose_next()

            self.state.president = chosen

        else:
            assert False, "Unrecognised action!"

    def finish_game(self):
        if self.hitler.is_dead:
            for x in [player for player in self.state.players if not player.is_fascist]:
                self.stats.add_agent_win(x.name)
                #print("Liberals win by shooting Hitler!")
            return 2
        elif self.hitler_chancellor_win():
            #print("Fascists win by electing Hitler!")
            for x in [player for player in self.state.players if player.is_fascist]:
                self.stats.add_agent_win(x.name)
            return -2
        elif self.policy_win():
            if self.state.liberal_track == 5:
                for x in [player for player in self.state.players if not player.is_fascist]:
                    self.stats.add_agent_win(x.name)
                    #print("Liberals win by policy!")
                return 1
            else:
                for x in [player for player in self.state.players if player.is_fascist]:
                    self.stats.add_agent_win(x.name)
                #print("Fascists win by policy!")
                return -1



def newgame(statCollector):
    game = HitlerGame(10, statCollector)
    return game.play()


if __name__ == "__main__":
    games = {"Liberal_policy": 0, "Liberal_kill_Hitler": 0, "Fascist_policy": 0, "Fascist_elect_Hitler": 0}
    print("Beginning play.")
    statCollector = HitlerStats()
    numgames = 10
    for ii in tqdm(range(numgames)):
        # print(ii)
        r = newgame(statCollector)
        if r == -2:
            games["Fascist_elect_Hitler"] += 1
        elif r == -1:
            games["Fascist_policy"] += 1
        elif r == 1:
            games["Liberal_policy"] += 1
        elif r == 2:
            games["Liberal_kill_Hitler"] += 1

    print(games)
    print(str(games["Liberal_policy"] + games["Liberal_kill_Hitler"]) + ":" +
          str(games["Fascist_policy"] + games["Fascist_elect_Hitler"]))
    print("Random policies passed: " + str(statCollector.random_policies_played) + " (Random policies per game: " + str(statCollector.random_policies_played / numgames) + ")")
    print(str(statCollector.agent_wins))
    print(str(statCollector.agent_kills))
