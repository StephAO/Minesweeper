class Tile:
    ''' Tile class,
        pretty straightforward'''
    def __init__(self, i ,j):
        self.i = i
        self.j = j
        self.known = False
        self.is_mine = False
        self.marked = False
        self.minep = 2
        self.value = 0

    def increment(self):
        self.value += 1

    def set_mine(self):
        self.is_mine = True

    def set_probability(self, minep):
        self.minep = minep

    def __str__(self):
        return ("("+str(self.i)+","+str(self.j)+")")

    def __repr__(self):
        return ("("+str(self.i)+","+str(self.j)+")")