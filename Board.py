import math
import random

MINE_RATIO = 0.20
MINE = "*"
UNKNOWN = 0
KNOWN = 1
MARKED = 2

class Board:

    def __init__(self, N, M, mines = None):
        ''' Initialize a Board.
            A Board is composed of:
                NxM : dimensions
                mines : locations of mines
                board : 2D array representing the tiles (domain: {1,2,3,4,5,6,7,8,'*'})
                known : 2D boolean array representing which tiles are known to player
        '''

        self.N = N
        self.M = M
        if mines is None:
            number_mines = int(math.floor(N*M*MINE_RATIO))
            self.mines = self.randomize_mines(N,M,number_mines)
        else:
            self.mines = mines

        # value of the board
        self.board = []
        # boolean array of know tiles
        self.known = []
        for row in range(N):
            self.board.append([])
            self.known.append([])
            for col in range(M):
                self.board[row].append(0)
                self.known[row].append(UNKNOWN)

        for mine in self.mines:
            i = mine[0]
            j = mine[1]
            # set mine
            self.board[i][j] = MINE
            # adjust numbers adjacent
            for _i,_j in get_adjacent(i,j):
                if in_bounds(_i,_j,self.N,self.M) and self.board[_i][_j] != MINE:
                    self.board[_i][_j] += 1

        print(self.board)


    def randomize_mines(self,N,M,number_mines):
        ''' Generate random board '''
        row_index = 0
        col_index = 0
        i = 0
        added = []
        while i < number_mines:
            row_index = (row_index+random.randint(0,N))%N
            col_index = (col_index+random.randint(0,M))%M
            if (row_index,col_index) not in added:
                added.append((row_index,col_index))
                i += 1
        return added

    def select(self,i,j,flag):
        ''' Returns a list of uncovered tiles'''
        if flag:
            print("MARKED")
            self.known[i][j] = MARKED
            return True
        if self.known[i][j] == KNOWN:
            print("ALREADY KNOWN")
            return True
        if self.board[i][j] == MINE:
            self.known[i][j] = KNOWN
            print("GAME OVER")
            return False
        self.uncover_recurse(i,j)
        return True

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

        recurse = self.board[i][j] == 0 and not self.known[i][j] == KNOWN
        self.known[i][j] = KNOWN
        if recurse:
            for _i,_j in get_adjacent(i,j):
                if in_bounds(_i,_j,self.N,self.M):
                    self.uncover_recurse(_i,_j)

    def solved(self):
        ''' Checks to see if all known non-mine tiles are known '''
        solved = True
        for i in range(self.N):
            for j in range(self.M):
                if self.known[i][j] == KNOWN:
                    if self.board[i][j] == MINE:
                        solved = False
                else:
                    if not self.board[i][j] == MINE:
                        solved = False
        return solved


    def __repr__(self):
        return "Board"

    def __str__(self):
        string = ""
        for i in range(self.N):
            for j in range(self.M):
                if self.known[i][j] == UNKNOWN:
                    string += "[ ]"
                if self.known[i][j] == KNOWN:
                    string += (" "+str(self.board[i][j])+" ")
                if self.known[i][j] == MARKED:
                    string += ("[X]")
##                string += " "+str(self.board[i][j])+" " #if self.known[i][j] else "[ ]"
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

