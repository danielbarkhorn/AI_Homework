# Dan Barkhorn, HW 1
# COEN 266, Prof. Conner
# 4-30-17
# This implementation of bbfs search is basically two A* searches trying to find one another.
# Note the ordering @ line 30 that ensures cost is still computed from 'start's' point of view
# Also note greatly improved performance for test map 4, and the severely worsened performance
# on test map 2. I believe on map 2 the searches chase one another and take a  convoluted routes.


import environment
import state

class Search:
    openSetS = []
    closedSetS = []
    openSetE = []
    closedSetE = []

    def __init__(self, start_pos, environment):
        self.environment = environment
        self.start = state.State(start_pos.x, start_pos.y)
        self.end = state.State(environment.end_x, environment.end_y)

    # Return a triplet of solution, openSet, and closedSet
    def search(self):
        self.start.heuristic = self.environment.bbfs_Heuristic(self.start, self.end)
        self.start.fScore = self.start.cost_so_far + self.start.heuristic
        self.openSet_append(self.openSetS, self.closedSetS, self.start)

        self.end.heuristic = self.environment.bbfs_Heuristic(self.start, self.end) #note ordering
        self.end.fScore = self.end.cost_so_far + self.end.heuristic
        self.openSet_append(self.openSetE, self.closedSetE, self.end)

        while len(self.openSetS)!=0 and len(self.openSetE) != 0:
            bestS = self.best_elem(self.openSetS, self.closedSetS) #this takes care of removing it from openSet
            bestE = self.best_elem(self.openSetE, self.closedSetE)
            if(bestE.x == bestS.x and bestE.y == bestS.y):
                #print('Dan\'s print\n', self.openSet)
                return (self.bbfs_Answer(bestS, bestE))
            availS = self.environment.available_moves(bestS)
            availE = self.environment.available_moves(bestE)
            for i in availS:
                i.heuristic = self.environment.bbfs_Heuristic(i, bestE)
                i.fScore = i.heuristic + i.cost_so_far
                self.openSet_append(self.openSetS, self.closedSetS, i)
            for i in availE:
                i.heuristic = self.environment.bbfs_Heuristic(i, bestS)
                i.fScore = i.heuristic + i.cost_so_far
                self.openSet_append(self.openSetE, self.closedSetE, i)

    def best_elem(self, OS, CS):
        #because oldest elems are at front of the list, and added in NESW order, this implementation should be ok
        best = OS[0]
        for i in OS:
            if(i.fScore < best.fScore):
                best = i
        OS.remove(best)
        CS.append(best)
        return best

    def openSet_append(self, OS, CS, new_State):
        for i in CS:
            if(i.x == new_State.x and i.y == new_State.y):
                return
        for i in OS:
            if(i.x == new_State.x and i.y == new_State.y):
                if(i.fScore > new_State.fScore):
                    OS.remove(i)
                    OS.append(new_State)
                    return
                else:
                    return
        OS.append(new_State)

    # Implement!
    def bbfs_Answer(self, start, end):
        openSet = self.openSetS + self.openSetE
        closedSet = self.closedSetS + self.closedSetE
        final = state.State(self.environment.end_x, self.environment.end_y)
        final.cost_so_far = start.cost_so_far + end.cost_so_far
        for i in end.moves_so_far:
            if(i == 'N'):
                start.moves_so_far.append('S')
            elif(i=='E'):
                start.moves_so_far.append('W')
            elif(i=='S'):
                start.moves_so_far.append('N')
            elif(i=='W'):
                start.moves_so_far.append('E')
        final.moves_so_far = start.moves_so_far

        return (final, openSet, closedSet)
