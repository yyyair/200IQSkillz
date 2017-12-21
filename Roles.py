class SmartPirate:

    ERROR_PIRATE_NOT_IN_PUSH_RANGE = 1
    ERROR_PIRATE_PUSHED_TOO_FAR = 2
    ERROR_PUSH_COOLDOWN = 3

    def __init__(self, pirate, game):
        self._game = game
        self._pirate = pirate
        self.id = self._pirate.id
        self.last_turn = -1
        self.waypoints = []

        self.movement_mode = "DEST"  # DEST means moves to a destination, TARGET means moves to a target
        self.target = None
        self.repeat = False
        self.sp = -1

    # Attempts to move the pirate towards its current set destination
    def move(self):
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


    def push(self, target, dest):
        if self.last_turn != self._game.turn:
            if self._pirate.in_push_range(target):
                if target.distance(dest) > self._pirate.push_range:
                    if self._pirate.push_reload_turns == 0:
                        self._pirate.push(target, dest)
                        self.last_turn = self._game.turn

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
    pass

class Carrier(Worker):
    def __init__(self, pirate):
        Worker.__init__(self,pirate, Roles["carrier"])
        self.repeat = True
        self.add_dest(pirate._game.get_my_mothership().get_location())
        self.add_dest(pirate._game.get_my_capsule().initial_location)





class Escort(Worker):
    pass

Roles = {
    "carrier":{"_class":Carrier, "IRole": IRole([1,1,1],[1,1,1], 0)},
    "camper":{"_class":Escort, "IRole": IRole([1,1,1],[1,1,1], 0)},
    "escort":{"_class":Escort, "IRole": IRole([1,1,1],[1,1,1], 0)}
}
RoleList = [Carrier]

