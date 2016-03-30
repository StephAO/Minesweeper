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

##        print(self.board)

    def randomize_mines(self):
        ''' Generate random board '''
        row_index = 0
        col_index = 0
        i = 0
        added = []
        while i < self.number_mines:
            row_index = (row_index+random.randint(0,self.N))%self.N
            col_index = (col_index+random.randint(0,self.M))%self.M
            if (row_index,col_index) not in added:
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

    def check_constraint(self,tile):
        '''
            Checks tile to see if see any information can be gained.
            Checks the value of the tile and compares it to the tile around it.
            If number of known mines in the adjacent tiles is equal to the value the tile is deemed safe
            If the number of unknown tiles is equal to the value, the tile is deemed unsafe
            Sets the probability of all unknown adjacent mines to number of mines remaining/number of unknown tiles
            Returns the safe tiles, the unsafe tiles, and the tiles who's probability has been set
        '''
        if not tile.known:
##            print("TILE NOT KNOWN")
            return [], [], []
        if tile.is_mine:
##            print("TILE IS MINE")
            return [], [], []
        mines_remaining = tile.value
        number_unknown = 0
        for adj_tile in self.get_adjacent(tile):
            mines_remaining -= 1 if (adj_tile.known and adj_tile.is_mine) or adj_tile.marked else 0
##            print(adj_tile.known)
            number_unknown += 0 if adj_tile.known or adj_tile.marked else 1

        if number_unknown == 0:
##            print("All adjacent tiles known")
            return [], [], []

        safe = (mines_remaining == 0)
        unsafe = (mines_remaining == number_unknown)
        minep = mines_remaining/number_unknown

        safe_tiles = []
        unsafe_tiles = []
        prob_tiles = []

        for adj_tile in self.get_adjacent(tile):
            if not adj_tile.known and not adj_tile.marked:
                if minep < adj_tile.minep:
                    adj_tile.set_probability(minep)
                    prob_tiles.append(adj_tile)
                if safe:
                    safe_tiles.append(adj_tile)
                elif unsafe:
                    unsafe_tiles.append(adj_tile)

        return safe_tiles, unsafe_tiles, prob_tiles

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

    def solved(self):
        ''' Checks to see if all unknown tiles are mines '''
        return self.unknown_tiles == 0

    def check_sol(self):
        ''' checks to see if we are right '''
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
            ''' Returns a list of adjacent tiles. '''
            i = tile.i
            j = tile.j
            adj = [(i+1,j+1),(i+1,j),(i+1,j-1),(i,j-1),(i-1,j-1),(i-1,j),(i-1,j+1),(i,j+1)]
            return [self.board[_i][_j] for _i,_j in adj if self.in_bounds(_i,_j)]

