from pirates import *
from PirateManager import PirateHandler
from Challenges import ChallengeList, do_challenge
from Oracle import Oracle

PHandle = None
POracle = None
def init(game):
    global PHandle
    global POracle
    PHandle = PirateHandler(game)
    POracle = Oracle(game)
    # Test code
    #game.debug(PHandle.groups)

    PHandle.groups[0].regroup(Location(0,0))
    PHandle.groups[0].regroup(Location(440,4400))
    PHandle.set_pirate_role(0, "carrier")
    PHandle.debug(game)
    #game.debug(POracle.assign_roles(PHandle))




def do_turn(game):

    global PHandle
    # If it's a challenge bot, direct to Ron's code
    if game.get_enemy().bot_name in ChallengeList:
        do_challenge(game)
        return
    # Init on first turn only
    if game.turn == 1:
        init(game)

    ''' CODE STARTS HERE '''

    game.debug(PHandle.groups)
    for group in PHandle.groups:
        group.move()
    # Execute game plan
    # something.update(


