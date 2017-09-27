#!/usr/bin/python

import sys
import state
import astar

class Environment:
    'Map-based environment'

    # Member data
    # elevations: raw data for each position, stored in a list of lists
    #             (each outer list represents a single row)
    # height: number of rows
    # width: number of elements in each row
    # end_x, end_y: location of goal

    def __init__(self, mapfile, energy_budget, end_coords):
        self.elevations = []
        self.height = 0
        self.width = -1
        self.end_x, self.end_y = end_coords
        self.energy_budget = energy_budget
        # Read in the data
        for line in mapfile:
            nextline = [ int(x) for x in line.split() ]
            if self.width == -1:
                self.width = len(nextline)
            elif len(nextline) == 0:
                sys.stderr.write("No data (or parse error) on line %d\n"
                                 % (len(self.elevations) + 1))
                sys.exit(1)
            elif self.width != len(nextline):
                sys.stderr.write("Inconsistent map width in row %d\n"
                                 % (len(self.elevations) + 1))
                sys.stderr.write("Expected %d elements, saw %d\n"
                                 % (self.width, len(nextline)))
                sys.exit(1)
            self.elevations.insert(0, nextline)
        self.height = len(self.elevations)
        if self.end_x == -1:
            self.end_x = self.width - 1
        if self.end_y == -1:
            self.end_y = self.height - 1

    # Determine if state is a goal state or not
    def is_goal_state(self, state):
        return (state.x == self.end_x and state.y == self.end_y)

    # Calculate available moves from state
    # Return as list of states
    def available_moves(self, curr_state):
        availMoves = []
        if(curr_state.y != self.height-1):
            north = state.State(curr_state.x, curr_state.y+1)
            north.cost_so_far = self.compute_cost(curr_state, north)
            north.moves_so_far = curr_state.moves_so_far + ['N']
            availMoves.append(north)
        if(curr_state.x != self.width-1):
            east = state.State(curr_state.x+1, curr_state.y)
            east.cost_so_far = self.compute_cost(curr_state, east)
            east.moves_so_far = curr_state.moves_so_far + ['E']
            availMoves.append(east)
        if(curr_state.y != 0):
            south = state.State(curr_state.x, curr_state.y-1)
            south.cost_so_far = self.compute_cost(curr_state, south)
            south.moves_so_far = curr_state.moves_so_far + ['S']
            availMoves.append(south)
        if(curr_state.x != 0):
            west = state.State(curr_state.x-1, curr_state.y)
            west.cost_so_far = self.compute_cost(curr_state, west)
            west.moves_so_far = curr_state.moves_so_far + ['W']
            availMoves.append(west)
        return availMoves

    def heuristic(self, current_state):
        x_dif = abs(self.end_x - current_state.x)
        y_dif = abs(self.end_y - current_state.y)
        elevation_dif = abs(self.elevations[self.end_y][self.end_x] - self.elevations[current_state.y][current_state.x])
        return x_dif + y_dif + elevation_dif

    def bbfs_Heuristic(self, current_state, goal_state):
        x_dif = abs(goal_state.x - current_state.x)
        y_dif = abs(goal_state.y - current_state.y)
        elevation_dif = abs(self.elevations[goal_state.y][self.end_x] - self.elevations[goal_state.y][current_state.x])
        return x_dif + y_dif + elevation_dif

    def compute_cost(self, old_state, new_state):
        old_el = self.elevations[old_state.y][old_state.x]
        new_el = self.elevations[new_state.y][new_state.x]
        final = 0
        if(new_el == old_el):
            final = 1
        elif(new_el >= old_el):
            final = (1 + (new_el - old_el)**2)
        elif(old_el >= new_el):
            final = (1 + (old_el - new_el))
        #want this cost plus the previous?
        final += old_state.cost_so_far

        return final
