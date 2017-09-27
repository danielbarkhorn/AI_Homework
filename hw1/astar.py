# Dan Barkhorn, HW 1
# COEN 266, Prof. Conner
# 4-20-17

import environment
import state

class Search:
    openSet = []
    closedSet = []

    def __init__(self, start_pos, environment):
        self.environment = environment
        self.start = state.State(start_pos.x, start_pos.y)

    # Return a triplet of solution, openSet, and closedSet
    def search(self):
        self.start.heuristic = self.environment.heuristic(self.start)
        self.start.fScore = self.start.cost_so_far + self.start.heuristic
        self.openSet_append(self.start)
        best = self.start
        while len(self.openSet)!=0:
            best = self.best_elem() #this takes care of removing it from openSet
            if(self.environment.is_goal_state(best)):
                return (best, self.openSet, self.closedSet)
            avail = self.environment.available_moves(best)
            for i in avail:
                i.heuristic = self.environment.heuristic(i)
                i.fScore = i.heuristic + i.cost_so_far
                self.openSet_append(i)
        return (best, self.openSet, self.closedSet)

    def best_elem(self):
        #because oldest elems are at front of the list, and added in NESW order, this implementation should be ok
        best = self.openSet[0]
        for i in self.openSet:
            if(i.fScore < best.fScore):
                best = i
        self.openSet.remove(best)
        self.closedSet.append(best)
        return best

    def openSet_append(self, new_State):
        for i in self.closedSet:
            if(i.x == new_State.x and i.y == new_State.y):
                return
        for i in self.openSet:
            if(i.x == new_State.x and i.y == new_State.y):
                if(i.fScore > new_State.fScore):
                    self.openSet.remove(i)
                    self.openSet.append(new_State)
                    return
                else:
                    return
        self.openSet.append(new_State)
