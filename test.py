import Board
import Tile

def add(a):
    a.append(5)

def main():
    b = Board.Board(6,6) # [(1,1),(2,2),(3,4),(2,4)]
    probability_of_success = 1
    while not b.solved():
        loc = []
        q = False
        while len(loc) < 2:
            loc = input("Please enter a 0-indexed location. (row,col): ")
            if loc[0].lower() == 'q' or loc[0].lower() == 'quit':
                q = True
                print("QUITTING GAME")
                break
        if q:
            break
        print(loc)
        loc = loc.split(',')
        mark = None if len(loc) == 2 else True
        # the function to update pmine has not been added yet
        uncovered_tiles = b.select(int(loc[0]), int(loc[1]), mark)
        print(b)
        safe_mines = []

        b.check_constraint(b.board[int(loc[0])][int(loc[1])])
        if safe_mines is not None:
            for sf in safe_mines:
                print("SAFE: ",sf)


    else:
        print("CONGRATULATIONS")


if __name__ == '__main__':
    main()
