import astar

class State:
    #self.x = 0
    #self.y =  0
    moves_so_far = []
    cost_so_far = 0

    def __init__(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos

    # This needs to be checked!
    def __str__(self):
        return 'Pos=(%s, %s) Moves=%s Cost=%s' % (self.x, self.y, self.moves_so_far, self.cost_so_far)
