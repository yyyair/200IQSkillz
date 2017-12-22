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
    '''PHandle.set_pirate_role(0, "camper").set_camp(game.get_enemy_mothership().get_location())
    PHandle.set_pirate_role(1, "camper").set_camp(game.get_enemy_mothership().get_location())
    PHandle.set_pirate_role(2, "camper").set_camp(game.get_enemy_mothership().get_location())
    PHandle.set_pirate_role(3, "carrier")
    #PHandle.set_camp(Location(300,300))'''
    PHandle.debug(game)
    game.debug([i.name for i in POracle.assign_roles(PHandle )])




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
    PHandle.update()
    # Execute game plan
    # something.update(


