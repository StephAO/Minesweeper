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
            self.mines = self.randomize_mines(N,M)
        else:
            self.mines = mines

        # value of the board
        self.board = []
        for row in range(N):
            self.board.append([])
            for col in range(M):
                self.board[row].append(Tile())

        for mine in self.mines:
            i = mine[0]
            j = mine[1]
            # set mine
            self.board[i][j].set_mine()
            # adjust numbers adjacent
            for _i,_j in get_adjacent(i,j):
                if in_bounds(_i,_j,self.N,self.M) and not self.board[_i][_j].is_mine:
                    self.board[_i][_j].increment()

##        print(self.board)


    def randomize_mines(self,N,M):
        ''' Generate random board '''
        row_index = 0
        col_index = 0
        i = 0
        added = []
        while i < self.number_mines:
            row_index = (row_index+random.randint(0,N))%N
            col_index = (col_index+random.randint(0,M))%M
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

        p = tile.minep
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
            return tile.minep

        # if selected is a valid non-mine tile
        self.uncover_recurse(i,j)
        return tile.minep

    def uncover_recurse(self,i,j):
        ''' Recursively uncover tiles that have no surrounding mines
            All edges should be numbers
            e.g.:

                [ ][ ][ ][ ][ ]     [ ][ ][ ][ ][ ]
                [ ][ ][ ][ ][ ]     [ ] 1  1  1 [ ]
                [ ][ ] 0 [ ][ ] ==> [ ] 1  0  1 [ ]
                [ ][ ][ ][ ][ ]     [ ] 1  1  1 [ ]
                [ ][ ][ ][ ][ ]     [ ][ ][ ][ ][ ]
        '''

        tile = self.board[i][j]
        recurse = tile.value == 0 and not tile.known
        if not tile.known:
            self.unknown_tiles -= 1
        tile.known = True
        if recurse:
            for _i,_j in get_adjacent(i,j):
                if in_bounds(_i,_j,self.N,self.M):
                    self.uncover_recurse(_i,_j)

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

def in_bounds(i,j,N,M):
    return i >= 0 and i < N \
        and j >= 0 and j < M

def get_adjacent(i,j):
        ''' Returns a list of adjacent tiles.
            Tiles are represented a tuple: (row,col)
        '''
        return [(i+1,j+1),(i+1,j),(i+1,j-1),(i,j-1),(i-1,j-1),(i-1,j),(i-1,j+1),(i,j+1)]

