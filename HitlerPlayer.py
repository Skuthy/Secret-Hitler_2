import HitlerConstants

class TableTalk(object):
    ## Object for players to make claims or assertions
    def __init__(self, make_assertion, make_pass_claim, make_passed_claim):
        self._make_assertion = make_assertion
        self._make_pass_claim = make_pass_claim
        self._make_passed_claim = make_passed_claim
        self._receive_assertion = None
        self._receive_pass_claim = None
        self._receive_passed_claim = None

    def make_assertion(self, playerid, role, confidence=100):
        # assert that playerid is role
        # role: 0 = liberal, 1 = fascist, 2 = hitler
        # confidence: 0 = no confidence, 100 = perfect confidence
        if (confidence < 0 or confidence > 100):
            raise Exception("Confidence must be in the range of 0-100")
        self._make_assertion(playerid, role, confidence)

    def make_pass_claim(self, claim, myPlayerid, destPlayerId):
        # claim that you passed one of a set of claims (see HitlerConstants)
        if claim not in HitlerConstants.pass_statements.keys():
            raise Exception("Pass claim invalid")
        self._make_pass_claim(claim, myPlayerid, destPlayerId)
    
    def make_passed_claim(self, claim, myPlayerId, srcPlayerId):
        # claim that playerid passed you one of two things
        if claim not in HitlerConstants.choice_statements.keys():
            raise Exception("Passed claim invalid")
        self._make_passed_claim(claim, myPlayerId, srcPlayerId)
    
    def set_assertion_receiver(self, receiver):
        # set handler for calls to make_assertion
        self._receive_assertion = receiver

    def set_pass_claim_receiver(self, receiver):
        self._receive_pass_claim = receiver

    def set_passed_claim_receiver(self, receiver):
        self._receive_passed_claim = receiver


class HitlerPlayer(object):
    def __init__(self, id, name, role, state):
        self.id = id
        self.name = name
        self.role = role
        self.state = state
        self.hitler = None
        self.fascists = []
        self.is_dead = False
        self.inspected_players = {}

    @property
    def is_fascist(self):
        return self.role.party_membership == "fascist"

    @property
    def is_hitler(self):
        return self.role.role == "hitler"

    @property
    def knows_hitler(self):
        return self.hitler is not None

    def __repr__(self):
        return ("HitlerPlayer id:%d, name:%s, role:%s" %
                (self.id, self.name, self.role))

    def nominate_chancellor(self):
        """
        Choose who you want to be chancellor!
        :return: HitlerPlayer
        """
        raise NotImplementedError("Player must be able to choose a chancellor")

    def filter_policies(self, policies):
        """
        As president, choose 2 of three policies to play
        :return: Tuple of (List[choice1, choice2], discarded)
        """
        raise NotImplementedError("Player must be able to filter policies as president")

    def veto(self):
        """
        Decide whether to veto an action or not
        :return: Boolean
        """
        raise NotImplementedError("Player must be able to veto a policy")

    def enact_policy(self, policies):
        """
        Decide which of two policies to enact
        :param policies: policies
        :return: Tuple of (chosen, discarded)
        """
        raise NotImplementedError("Player must be able to enact a policy as chancellor")

    def vote(self):
        """
        Vote for the current president + chancellor combination
        :return: Vote
        """
        raise NotImplementedError("Player must be able to vote!")

    def view_policies(self, policies):
        """
        What to do if you perform the presidential action to view the top three policies
        :return:
        """
        raise NotImplementedError("Player must react to view policies action")

    def kill(self):
        """
        Choose a person to kill
        :return:
        """
        raise NotImplementedError("Player must choose someone to kill")

    def inspect_player(self):
        """
        Choose a person's party membership to inspect
        :return:
        """
        raise NotImplementedError("Player must choose someone to inspect")

    def choose_next(self):
        """
        Choose the next president
        :return:
        """
        raise NotImplementedError("Player must choose next president")

class Vote(object):
    def __init__(self, type):
        self.type = type

    def __nonzero__(self):
        return self.type

    def __bool__(self):
        return self.type


class Ja(Vote):
    def __init__(self):
        super(Ja, self).__init__(True)


class Nein(Vote):
    def __init__(self):
        super(Nein, self).__init__(False)
