'''
File containing all classes related to role implementation. To create a new role:
1. Create a class that extends Worker
2. Add the class to RoleList and Roles
3. Add atributes and methods
4. Override update() to add logic
5. Adjust effectiveness stats and rewards/punishments (*)

*not fully implemented yet
'''
from pirates import Location
import math
class SmartPirate:

    ERROR_PIRATE_NOT_IN_PUSH_RANGE = 1
    ERROR_PIRATE_PUSHED_TOO_FAR = 2
    ERROR_PUSH_COOLDOWN = 3
    SUCCESS = 4

    def __init__(self, pirate, game):
        self._game = game
        self._pirate = pirate
        self.id = self._pirate.id
        # Last turn pirate did a legal action
        self.last_turn = -1

        self.waypoints = []
        # DEST means moves to a destination, TARGET means moves to a target
        self.movement_mode = "DEST"
        # Target to chase after
        self.target = None
        # If set to True, pirate will cycle waypoints instead of queueing them
        self.repeat = False
        # Waypoint stack pointer
        self.sp = -1

    # Attempts to move the pirate towards its current set destination
    def move(self):
        if self.movement_mode == "TARGET":
            if self.last_turn != self._game.turn:
                self._pirate.sail(self.target.get_location())
                self.last_turn = self._game.turn

        if not len(self.waypoints): return
        # Check if at current destination
        if self._pirate.get_location() == (self.waypoints[self.sp]):
            if not self.repeat:
                self.remove_dest()
            else:
                self.sp = (self.sp - 1) % len(self.waypoints)

        # Check if theres a destination
        if not len(self.waypoints): return

        # Check if can move
        if self.last_turn != self._game.turn:
            self._pirate.sail(self.waypoints[self.sp])
            self.last_turn = self._game.turn


    # Adds a destination for the queue
    def add_dest(self, dest):
        self.waypoints.append(dest)
        self.sp += 1

    # Removes the current destination from the queue
    def remove_dest(self):
        if len(self.waypoints):
            self.waypoints.remove(self.waypoints[-1])
            self.sp -= 1

    def update(self):
        self.move()


    def push(self, target, dest):
        if self.last_turn != self._game.turn:
            if self._pirate.in_push_range(target):
                if target.distance(dest) > self._pirate.push_range:
                    if self._pirate.push_reload_turns == 0:
                        self._pirate.push(target, dest)
                        self.last_turn = self._game.turn
                        return SmartPirate.SUCCESS

                else:
                    return SmartPirate.ERROR_PIRATE_PUSHED_TOO_FAR
            else:
                return SmartPirate.ERROR_PIRATE_NOT_IN_PUSH_RANGE

    def get_location(self):
        return self._pirate.get_location()



class IRole:
    def __init__(self, bv, bg, id):
        self.base_value = bv
        self.base_growth = bg
        self.eff = 1
        self.roleId = id

    def value(self):
        return [self.eff * self.base_growth[i] + self.base_value[i]
                for i in range(min(len(self.base_growth), len(self.base_value)))]

class Worker(SmartPirate):
    def __init__(self, pirate, role):
        self.role = role
        SmartPirate.__init__(self, pirate._pirate, pirate._game)


class Camper(Worker):

    IDLE = 1
    CHASE = 2
    REBASE = 3
    PATROL = 4

    def __init__(self, pirate):
        Worker.__init__(self,pirate, Roles["camper"]["IRole"])
        self.camp = None
        self.mode = None
        self.aggro_range = 1500
        self.idle_range = 500
        self.repeat = True

        self.set_camp(self._game.get_enemy_mothership().get_location())

    def update(self):
        if self.mode == Camper.IDLE:
            cap = self._game.get_enemy_capsule()
            if cap.holder is not None and not self._pirate.push_reload_turns:
                if self._pirate.in_range(cap.holder, self.aggro_range):
                    self.target = cap.holder
                    self.movement_mode = "TARGET"
                    self.mode = Camper.CHASE
        elif self.mode == Camper.CHASE:
            if self.push(self.target, Location(0,0)) == SmartPirate.SUCCESS:
                self.movement_mode = "DEST"
                self.mode = Camper.REBASE
        elif self.mode == Camper.REBASE:
            if self.at_camp():
                self.mode = Camper.IDLE
            else:
                print self.waypoints
                self.move()
        else:
            self.mode = Camper.REBASE
        print self.mode, self.movement_mode
        SmartPirate.update(self)

    def set_camp(self, location):
        self.remove_dest()
        self.add_dest(location)
        self.camp = location

    def at_camp(self):
        return self._pirate.in_range(self.camp, self.idle_range)

    pass

class Carrier(Worker):
    def __init__(self, pirate):
        Worker.__init__(self,pirate, Roles["carrier"]["IRole"])
        self.repeat = True
        self.add_dest(pirate._game.get_my_mothership().get_location())
        self.add_dest(pirate._game.get_my_capsule().initial_location)

    def update(self):
        '''
        code here
        '''
        SmartPirate.update(self)





class Escort(Worker):
    def __init__(self, pirate):
        Worker.__init__(self,pirate, Roles["escort"]["IRole"])
        self.repeat = True
        self.add_dest(pirate._game.get_my_mothership().get_location())
        self.add_dest(pirate._game.get_my_capsule().initial_location)

    def update(self):
        '''
        code here
        '''
        SmartPirate.update(self)

Roles = {
    "carrier":{"_class":Carrier, "IRole": IRole([10,1,50],[1,1,1], "carrier")},
    "camper":{"_class":Camper, "IRole": IRole([30,20,0],[1,1,1], "camper")},
    "escort":{"_class":Escort, "IRole": IRole([15,30,0],[1,1,1], "escort")}
}
RoleList = [Carrier, Camper, Escort]

