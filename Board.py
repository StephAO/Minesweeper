from Tile import *
import math
import random

MINE_RATIO = 0.20
MINE = "*"
UNKNOWN = -1
KNOWN = 0
MARKED = 1

class Board:

    def __init__(self, N, M, number_mines = None, mines = None):
        ''' Initialize a Board.
            A Board is composed of:
                NxM : dimensions
                mines : locations of mines
                board : 2D array of tiles (domain: {1,2,3,4,5,6,7,8,'*'})
        '''

        self.N = N
        self.M = M
        self.starting_tile = (int(N/2), int(M/2))
        self.known_mines = 0
        self.unknown_tiles = M*N
        self.mines_hit = 0
        if mines is None:
            if number_mines is None:
                self.number_mines = int(math.floor(N*M*MINE_RATIO))
            else:
                self.number_mines = number_mines
            self.mines = self.randomize_mines()
        else:
            self.number_mines = len(mines)
            self.mines = mines

        # value of the board
        self.board = []
        for row in range(N):
            self.board.append([])
            for col in range(M):
                self.board[row].append(Tile(row,col))

        for mine in self.mines:
            tile = self.board[mine[0]][mine[1]]
            # set mine
            tile.set_mine()
            # adjust numbers adjacent
            for adj_tile in self.get_adjacent(tile):
                adj_tile.increment()

    def reset(self):
        ''' reset board so that it's the exact same as it was right after
            initialization
        '''
        self.known_mines = 0
        self.unknown_tiles = self.M*self.N
        self.mines_hit = 0
        for tile in self.get_all_tiles():
            tile.known = False
            tile.marked = False
            tile.minep = 2

    def randomize_mines(self):
        ''' Generate random board '''
        row_index = 0
        col_index = 0
        i = 0
        added = []
        while i < self.number_mines:
            row_index = (row_index+random.randint(0,self.N))%self.N
            col_index = (col_index+random.randint(0,self.M))%self.M
            if (row_index,col_index) not in added and (row_index,col_index) != (self.starting_tile):
                added.append((row_index,col_index))
                i += 1
        return added

    def get_tile(self,i,j):
        ''' return the tile object with the given coordinates'''
        if not self.in_bounds(i,j):
            print("INVALID TILE")
            return None
        return self.board[i][j]

    def get_all_tiles(self):
        ''' return a list of all the tiles in the board'''
        tiles = []
        for i in range(self.N):
            for j in range(self.M):
                tiles.append(self.board[i][j])
        return tiles

    def first_tile_to_pick(self):
        return self.get_tile(self.starting_tile[0], self.starting_tile[1])

    def select(self,tile):
        ''' Select this tile revealing it's value (or mine if it is a mine)
            Changes tile knowledge to true
            Returns a list of uncovered tiles'''
        # checking a tile that is already known
        if tile.known:
            print("ALREADY KNOWN")
            return []

        # selected a mine
        if tile.is_mine:
            self.unknown_tiles -= 1
            tile.known = True
            self.known_mines += 1
            self.mines_hit += 1
            return [tile]
##            print("GAME OVER")

        # if selected is a valid non-mine tile
        uncovered_tiles = self.uncover_recurse(tile)
##        print(uncovered_tiles)
        return uncovered_tiles

    def uncover_recurse(self,tile):
        ''' Recursively uncover tiles that have no surrounding mines
            All edges should be numbers
            e.g.:

                [ ][ ][ ][ ][ ]     [ ][ ][ ][ ][ ]
                [ ][ ][ ][ ][ ]     [ ] 1  1  1 [ ]
                [ ][ ] 0 [ ][ ] ==> [ ] 1  0  1 [ ]
                [ ][ ][ ][ ][ ]     [ ] 1  1  1 [ ]
                [ ][ ][ ][ ][ ]     [ ][ ][ ][ ][ ]

            returns a list of uncovered tiles
        '''
        if tile.known:
            return []
        uncovered_tiles = [tile]
        self.unknown_tiles -= 1
        tile.known = True
        if tile.value == 0:
            for adj_tile in self.get_adjacent(tile):
                    uncovered_tiles.extend(self.uncover_recurse(adj_tile))
        return uncovered_tiles

    def check_simple_constraint(self,tile):
        ''' Checks simple constraints (i.e. only comparing tile value to number
            of known mines surrounding). For complex constraints see check complex constraints.

            Checks tile to see if see any information can be gained.
            Checks the value of the tile and compares it to the tile around it.
            If number of known mines in the adjacent tiles is equal to the value the tile is deemed safe
            If the number of unknown tiles is equal to the value, the tile is deemed unsafe
            Sets the probability of all unknown adjacent mines to number of mines remaining/number of unknown tiles
            Returns the safe tiles, the unsafe tiles, and the tiles who's probability has been set
        '''
        if not tile.known:
            return [], [], []
        if tile.is_mine:
            return [], [], []
        mines_remaining = tile.value
        number_unknown = 0
        for adj_tile in self.get_adjacent(tile):
            mines_remaining -= 1 if (adj_tile.known and adj_tile.is_mine) or adj_tile.marked else 0
            number_unknown += 0 if adj_tile.known or adj_tile.marked else 1

        if number_unknown == 0:
            return [], [], []

        safe = (mines_remaining == 0)
        unsafe = (mines_remaining == number_unknown)
        minep = mines_remaining/number_unknown

        # return list
        safe_tiles = []
        unsafe_tiles = []
        prob_tiles = []

        for adj_tile in self.get_adjacent(tile):
            if not adj_tile.known and not adj_tile.marked:
                if adj_tile.minep == 2 or minep > adj_tile.minep:
                    adj_tile.set_probability(minep)
                    prob_tiles.append(adj_tile)
                if safe:
                    safe_tiles.append(adj_tile)
                elif unsafe:
                    unsafe_tiles.append(adj_tile)

        return safe_tiles, unsafe_tiles, prob_tiles

    def check_complex_constraint(self, tile):
        ''' Check complex constraints. These are any constraints beyond simple
            constraints (see simple constraints). They work primarily on the
            basis of groups of tiles with size > n, that required exactly, or
            less than n. From this information, it is sometimes possible to
            mark safe or unsafe tiles.

            Returns safe tiles, unsafe tiles, and tiles whose minep has changed
        '''
        # check to see if legal
        if not tile.known:
            return [], [], []
        if tile.is_mine:
            return [], [], []

        # constraints. List of lists. Inner lists are constraints
        # first element of constraints is n, remainder of elements are the tiles
        # the constraint is placed on
        exactly_n = []
        at_most_n = []

        # info about this tile
        adj_unknown = []
        num_mines = 0

        adj_tiles = self.get_adjacent(tile)
        for adj_tile in adj_tiles:
            if adj_tile.known:
                if adj_tile.is_mine:
                    num_mines += 1
                else:
                    adj2_unknown, adj2_rem_mines = self.get_remaining_info(adj_tile)
                    if len(adj2_unknown) == 0:
                        continue
                    # n = adj2_rem_mines
                    constraint = [adj2_rem_mines]
                    unknowns_inside_adjacent = [u for u in adj2_unknown if (u in adj_tiles)]
                    constraint.extend(unknowns_inside_adjacent)
                    # all adj_unknowns are in tile adjacents
                    if len(unknowns_inside_adjacent) == len(adj2_unknown):
                        exactly_n.append(constraint)
                    else:
                        at_most_n.append(constraint)
            else:
                if adj_tile.marked:
                    num_mines += 1
                else:
                    adj_unknown.append(adj_tile)

        num_mines_rem = tile.value - num_mines
        num_unknown = len(adj_unknown)
        if num_unknown == 0:
            return [],[],[]

        # return list
        safe_tiles = []
        unsafe_tiles = []
        prob_tiles = []

        # apply constraints
        for constraint in exactly_n:
            n = constraint.pop(0)
            other_unknowns = [at for at in adj_unknown if at not in constraint]
            if len(other_unknowns) == 0:
                continue
            minep = (num_mines_rem-n)/len(other_unknowns)
            if num_mines_rem == n:
                safe_tiles.extend(other_unknowns)
            elif (num_mines_rem-n) == len(other_unknowns):
                unsafe_tiles.extend(other_unknowns)
            else:
                for ou in other_unknowns:
                    if ou.minep == 2 or minep > ou.minep:
                        ou.set_probability(minep)
                        prob_tiles.append(ou)

        for constraint in at_most_n:
            n = constraint.pop(0)
            other_unknowns = [at for at in adj_unknown if at not in constraint]
            if len(other_unknowns) == 0 or n > num_mines_rem:
                continue
            if (num_mines_rem-n) == len(other_unknowns):
                unsafe_tiles.extend(other_unknowns)

        return safe_tiles, unsafe_tiles, prob_tiles

    def get_remaining_info(self, tile):
        ''' Helper function'''
        if not tile.known:
            print("CAN'T GET INFO ON UNKNOWN TILES")
            return
        if tile.is_mine:
            print("CAN't GEt INFO FROM MINE TILE")
        unknown = []
        num_mines = 0
        for adj_tile in self.get_adjacent(tile):
            if (adj_tile.known and adj_tile.is_mine) or adj_tile.marked:
                num_mines += 1
            elif not adj_tile.known:
                unknown.append(adj_tile)
        return unknown, tile.value-num_mines

    def mark(self, tile):
        ''' Mark a tile as unsafe (i.e. we think it is a mine)'''
        if tile.marked:
            pass
##            self.unknown_tiles += 1
##            self.known_mines -= 1
        else:
            self.unknown_tiles -= 1
            self.known_mines += 1
        tile.marked = True
        tile.set_probability(1)

    # NEW VERSION
    def solved(self):
        ''' checks to see if we have solved the board '''
        for i in range(self.N):
            for j in range(self.M):
                if not self.board[i][j].is_mine and not self.board[i][j].known:
                    return False
        return True

    def __repr__(self):
        return "Board"

    def __str__(self):
        string = ""
        for i in range(self.N):
            for j in range(self.M):
                tile = self.board[i][j]
                if tile.known:
                    string += " * " if tile.is_mine else (" "+str(tile.value)+" ")
                elif tile.marked:
                    string += ("[X]")
                else:
                    string += "[ ]"
            string += "\n"
        return string


    def in_bounds(self,i,j):
        ''' Checks to see if a tile is within the board '''
        return i >= 0 and i < self.N \
            and j >= 0 and j < self.M

    def get_adjacent(self,tile):
            ''' Returns a list of adjacent tiles.
                order: starting bottom right going clockwise'''
            i = tile.i
            j = tile.j
            adj = [(i+1,j+1),(i+1,j),(i+1,j-1),(i,j-1),(i-1,j-1),(i-1,j),(i-1,j+1),(i,j+1)]
            return [self.board[_i][_j] for _i,_j in adj if self.in_bounds(_i,_j)]

