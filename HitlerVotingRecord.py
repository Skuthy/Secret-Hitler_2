from HitlerException import HitlerException
from HitlerPlayer import Ja, Nein

class HitlerVotingRecord():
    def __init__(self):
        # new record
        pass

    class VoteOutcome():
        def __init__(self):
            self.passed = False
            self.votes = {}
            self.outcome = -1
        
        def set_outcome(self, outcome):
            if outcome < 0 or outcome > 2:
                raise HitlerException("Unimplemented outcome specified.")
            self.outcome = outcome
        
        def add_vote(self, player, vote):
            if not (isinstance(vote, Ja)) and not (isinstance(vote, Nein)):
                raise HitlerException("Not a vote!")
            self.votes[player] = vote
            
