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
