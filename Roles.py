from PirateManager import SmartPirate

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
        SmartPirate.__init__(self, pirate, pirate._game)


class Camper(Worker):
    pass

class Carrier(Worker):
    def __init__(self, pirate):

        Worker.__init__(self,pirate, Roles["carrier"])
        pass


class Escort(Worker):
    pass

Roles = {
    "carrier":{"_class":Escort, "IRole": IRole([1,1,1],[1,1,1], 0)},
    "camper":{"_class":Escort, "IRole": IRole([1,1,1],[1,1,1], 0)},
    "escort":{"_class":Escort, "IRole": IRole([1,1,1],[1,1,1], 0)}
}
RoleList = [Carrier]

