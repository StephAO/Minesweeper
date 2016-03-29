from Tile import *
import math
import random

MINE_RATIO = 0.20
MINE = "*"
UNKNOWN = -1
KNOWN = 0
MARKED = 1

class Board:

    def __init__(self, N, M, mines = None):
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
        if mines is None:
            self.number_mines = int(math.floor(N*M*MINE_RATIO))
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

    def select(self,i,j,flag):
        ''' Returns a list of uncovered tiles'''
        # checking a tile that is already known
        tile = self.board[i][j]
        if tile.known:
            print("ALREADY KNOWN")
            return -1

        # marking down probabilities of tile being a mine
        if flag:
            self.unknown_tiles -= 1
            print("MARKED")
            tile.marked = True
            self.known_mines += 1
            return -1

        # selected a mine
        if tile.is_mine:
            self.unknown_tiles -= 1
            tile.known = True
            self.known_mines += 1
##            print("GAME OVER")

        # if selected is a valid non-mine tile
        return self.uncover_recurse(tile)


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
        uncovered_tiles = []
        recurse = tile.value == 0 and not tile.known
        if not tile.known:
            self.unknown_tiles -= 1
        tile.known = True
        if recurse:
            uncovered_tiles.append(tile)
            for adj_tile in self.get_adjacent(tile):
                    uncovered_tiles.extend(self.uncover_recurse(adj_tile))
        return uncovered_tiles


    def check_constraint(self,tile):
        if not tile.known:
            print("Tile not known")
            return None
        if tile.is_mine:
            print("Tile is a mine")
            return None
        mines_remaining = tile.value
        number_unknown = 0
        for adj_tile in self.get_adjacent(tile):
            mines_remaining -= 1 if adj_tile.known and \
                (adj_tile.is_mine or adj_tile.marked) else 0
##            print(adj_tile.known)
            number_unknown += 0 if adj_tile.known else 1

        if number_unknown == 0:
            print("All adjacent tiles known")
            return None

        safe = (mines_remaining == 0)

        safe_tiles = []

        for adj_tile in self.get_adjacent(tile):
            if not adj_tile.known:
                adj_tile.set_probability(mines_remaining/number_unknown)
##                print(tile, " probability = ", mines_remaining/number_unknown)
                adj_tile.is_mine = safe
                if safe:
                    safe_tiles.append(adj_tile)

        return safe_tiles

    def solved(self):
        ''' Checks to see if all known non-mine tiles are known '''
        return self.unknown_tiles == 0

    def check_sol(self):
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
        return i >= 0 and i < self.N \
            and j >= 0 and j < self.M

    def get_adjacent(self,tile):
            ''' Returns a list of adjacent tiles.
                Tiles are represented a tuple: (row,col)
            '''
            i = tile.i
            j = tile.j
            adj = [(i+1,j+1),(i+1,j),(i+1,j-1),(i,j-1),(i-1,j-1),(i-1,j),(i-1,j+1),(i,j+1)]
            return [self.board[_i][_j] for _i,_j in adj if self.in_bounds(_i,_j)]

