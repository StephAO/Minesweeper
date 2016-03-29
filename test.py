import Board
import Tile
import sys

def add(a):
    a.append(5)

def main():
    human = False
    if len(sys.argv) == 1 and sys.argv[0] == "human":
        human = True
    b = Board.Board(16,30,99) # [(1,1),(2,2),(3,4),(2,4)]
    probability_of_success = 1

    if human:
        human_player(b)
    else:
        FC(b)


def FC(b):
    probability_of_success = 1
    safe_tiles = set()
    known_probabilities = set()
    unknown_probabilities = set(b.get_all_tiles())
    while not b.solved():

        tile = None
        if len(safe_tiles) > 0:
            # if there's a safe tile, select that one next
            tile = safe_tiles.pop()
            if tile.known:
                continue
        else:
            # otherwise pick the tile with the lowest probability
            base_probability = ((b.number_mines-b.known_mines)/b.unknown_tiles)
            kp = sorted(known_probabilities, key = lambda tile: tile.minep)
            if len(kp) + len(unknown_probabilities) == 0:
                print(b.unknown_tiles)
                print(b)
            if len(kp) > 0 and (kp[0].minep < base_probability or len(unknown_probabilities)==0):
                tile = kp[0]
                known_probabilities.remove(tile)
                if tile.known:
                    continue
                probability_of_success *= (1-tile.minep)
            else:
                tile = unknown_probabilities.pop()
                if tile.known:
                    continue
                probability_of_success *= (1-base_probability)

        uncovered_tiles = set(b.select(tile))

        check_tiles = set()
        check_tiles.update(uncovered_tiles)
        for ut in uncovered_tiles:
            check_tiles.update(b.get_adjacent(ut))


        while check_tiles:
            ct = check_tiles.pop()
##            print(ct)
            safe, unsafe, knownp = b.check_constraint(ct)
    ##            print(uncovered_tile, "SAFE: ", safe, " --> UNSAFE: ", unsafe)
            safe_tiles.update(safe)
            known_probabilities.update(knownp)
            unknown_probabilities.difference_update(knownp)
##            print(unsafe)
            for ust in unsafe:
                if not ust.marked:
                    b.mark(ust)
                    check_tiles.update(b.get_adjacent(ust))

##        print("SAFE TILES", safe_tiles)
##        input("hit enter for next move, ps = " + str(probability_of_success))

    print(b)
    print(str(probability_of_success*100) + "%")
    print(str(b.mines_hit) + " hit out of " + str(b.number_mines))




def human_player(b):
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
        tile = b.get_tile(int(loc[0]), int(loc[1]))
        if len(loc) > 2:
            b.mark(tile)
        # the function to update pmine has not been added yet
        uncovered_tiles = b.select(tile)
        safe_tiles = set()
        unsafe_tiles = set()

        for uncovered_tile in uncovered_tiles:
            safe, unsafe = b.check_constraint(uncovered_tile)
    ##            print(uncovered_tile, "SAFE: ", safe, " --> UNSAFE: ", unsafe)
            safe_tiles.update(safe)
            unsafe_tiles.update(unsafe)

        for unsafe_tile in unsafe_tiles:
            b.mark(unsafe_tile)

        print(b)


if __name__ == '__main__':
    main()
