from pirates import *
from Roles import *

class Oracle:
    # Magic constant, should work
    m_func = lambda x, y, z: x*y*z

    def __init__(self, game):
        self.game = game

    # Assigns each pirate a role
    def assign_roles(self, phandle):
        items = []
        for pirate in phandle.get_all_my_pirates():
            items += [role(pirate) for role in RoleList]
        return items


class KnapsackObject:
    def __init__(self, value, weight, type):
        self.value = value
        self.weight = weight
        self.type = type

    def efficiency(self):
        return Oracle.m_func(self.weight[0], self.weight[1], self.weight[2])/float(sum(self.weight))

    def __str__(self):
        return "{" + str(self.value) + "," + str(self.weight) + "," +  str(self.efficiency())+"}"

class PirateMCKP(IRole, KnapsackObject):
    def efficiency(self):
        return Oracle.m_func(self.weight[0], self.weight[1], self.weight[2])/float(sum(self.weight))


"""
Finds a subset S of objs such that the sum value of S is maximal
:param objs: Objects
:param limits: Knapsack cieling weight values
"""
def knapsack(objs, limits):
    objs = sort(objs)
    sack = []
    sackObjs = []
    currentWeight = [0] * len(limits)
    for obj in objs:
        newWeight = [currentWeight[i] + obj.weight[i] for i in range(min(len(obj.weight), len(currentWeight)))]
        if obj.type in sack:
            pass
        elif all(newWeight[i] < limits[i] for i in range(len(limits))):
            sackObjs.insert(0, obj)
            sack.append(obj.type)
    return sackObjs
    pass

"""
Recursively selects a role for each item
:param items: All items available for selection
:param current: Currently selected pirates
"""
def choose_roles(items, current):
    if items == []:
        return current

    items = sort(items)
    added = items[0]
    current.append(added)
    n_items = []
    for item in items:
        if item.type == added.type:
            pass
        else:
            item.weight = [item.weight[i] + added.weight[i] for i in range(len(item.weight))]
            n_items.append(item)
    return choose_roles(n_items, current)



def sort(nums):
    nums = sorted(nums, key=lambda obj: obj.efficiency(), reverse=True)
    return nums

