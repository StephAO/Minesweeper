import Board
import Tile
import time
import sys
import csv

class MineSweeperCSP:

    def __init__(self):
        self.CSP_functions = [self.simpleFC, self.simpleGAC, self.complexFC, self.complexGAC, self.complexGAC_max_c]

    def run(self, fn, board, show=False):
        stime = time.clock()
        p = fn(board, show=show)
        time_taken = time.clock() - stime
        if show:
            print("Probability of success =",str(p*100)+"%","\nMines hit",board.mines_hit,"/",board.number_mines)
        num_mines = board.mines_hit
        board.reset()
        return p*100, num_mines, time_taken

    def run_all(self, board, mine_count, prob_succ, time_taken):
        mc = []
        ps = []
        tt = []

        for fn in self.CSP_functions:
            p, m, t = self.run(fn, board)
            ps.append(str(p))
            mc.append(str(m))
            tt.append(str(t))

        mine_count.writerow(mc)
        prob_succ.writerow(ps)
        time_taken.writerow(tt)

    def simpleFC(self, b, show):
        probability_of_success = 1
        safe_tiles = set()
        known_probabilities = set()
        unknown_probabilities = set(b.get_all_tiles())
        first = True
        while not b.solved():

            tile = None
            if first:
                tile = b.first_tile_to_pick()
                first = False
            elif len(safe_tiles) > 0:
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

            # get tiles to check constraints on
            check_tiles = set()
            check_tiles.update(uncovered_tiles)
            for ut in uncovered_tiles:
                check_tiles.update(b.get_adjacent(ut))

            # check constraints
            while check_tiles:
                ct = check_tiles.pop()
                safe, unsafe, knownp = b.check_simple_constraint(ct)
                safe_tiles.update(safe)
                known_probabilities.update(knownp)
                unknown_probabilities.difference_update(knownp)
                # mark tiles that are believed to be mines
                for ust in unsafe:
                    if not ust.marked:
                        b.mark(ust)

            if show:
                print(b)
                if (input('press enter to see next move, or q to quit') == 'q'):
                    break

        return probability_of_success

    def simpleGAC(self, b, show):
        probability_of_success = 1
        safe_tiles = set()
        known_probabilities = set()
        unknown_probabilities = set(b.get_all_tiles())
        first = True
        while not b.solved():

            tile = None
            if first:
                tile = b.first_tile_to_pick()
                first = False
            elif len(safe_tiles) > 0:
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

            # get tiles to check constraints on
            check_tiles = set()
            check_tiles.update(uncovered_tiles)
            for ut in uncovered_tiles:
                check_tiles.update(b.get_adjacent(ut))

            # check constraints
            while check_tiles:
                ct = check_tiles.pop()
                safe, unsafe, knownp = b.check_simple_constraint(ct)
                safe_tiles.update(safe)
                known_probabilities.update(knownp)
                unknown_probabilities.difference_update(knownp)
                # mark tiles that are believed to be mines
                for ust in unsafe:
                    if not ust.marked:
                        b.mark(ust)
                        # check constraints for all tiles adjacent to new marking
                        check_tiles.update(b.get_adjacent(ust))

            if show:
                print(b)
                if (input('press enter to see next move, or q to quit') == 'q'):
                    break

        return probability_of_success

    def complexFC(self, b, show):
        probability_of_success = 1
        safe_tiles = set()
        known_probabilities = set()
        unknown_probabilities = set(b.get_all_tiles())
        first = True
        while not b.solved():

            tile = None
            if first:
                tile = b.first_tile_to_pick()
                first = False
            elif len(safe_tiles) > 0:
##                print("picking a safe tile")
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

            # get tiles to check constraints on
            check_tiles = set()
            check_tiles.update(uncovered_tiles)
            for ut in uncovered_tiles:
                check_tiles.update(b.get_adjacent(ut))
                safe_tiles.discard(ut)

            # check constraints
            while check_tiles:
                ct = check_tiles.pop()
                unsafe = set()
                ssafe, sunsafe, sknownp = b.check_simple_constraint(ct)
                csafe, cunsafe, cknownp = b.check_complex_constraint(ct)
                safe_tiles.update(ssafe)
                safe_tiles.update(csafe)
                known_probabilities.update(sknownp)
                known_probabilities.update(cknownp)
                unknown_probabilities.difference_update(sknownp)
                unknown_probabilities.difference_update(cknownp)
                # mark tiles that are believed to be mines
                unsafe.update(sunsafe)
                unsafe.update(cunsafe)
                for ust in unsafe:
                    if not ust.marked:
                        b.mark(ust)

            if show:
                print(b)
                if (input('press enter to see next move, or q to quit') == 'q'):
                    break

        return probability_of_success


    def complexGAC(self, b, show):
        probability_of_success = 1
        safe_tiles = set()
        known_probabilities = set()
        unknown_probabilities = set(b.get_all_tiles())
        first = True
        while not b.solved():

            tile = None
            if first:
                tile = b.first_tile_to_pick()
                first = False
            elif len(safe_tiles) > 0:
##                print("picking a safe tile")
                # if there's a safe tile, select that one next
                tile = safe_tiles.pop()
                if tile.known:
                    continue
            else:
                # otherwise pick the tile with the lowest probability
                base_probability = ((b.number_mines-b.known_mines)/b.unknown_tiles)
                kp = sorted(known_probabilities, key = lambda tile: tile.minep)
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

            # get tiles to check constraints on
            check_tiles = set()
            check_tiles.update(uncovered_tiles)
            for ut in uncovered_tiles:
                check_tiles.update(b.get_adjacent(ut))
                safe_tiles.discard(ut)

            # check constraints
            while check_tiles:
                ct = check_tiles.pop()
                unsafe = set()
                ssafe, sunsafe, sknownp = b.check_simple_constraint(ct)
                csafe, cunsafe, cknownp = b.check_complex_constraint(ct)
                safe_tiles.update(ssafe)
                safe_tiles.update(csafe)
                known_probabilities.update(sknownp)
                known_probabilities.update(cknownp)
                unknown_probabilities.difference_update(sknownp)
                unknown_probabilities.difference_update(cknownp)
                # mark tiles that are believed to be mines
                unsafe.update(sunsafe)
                unsafe.update(cunsafe)
                for ust in unsafe:
                    if not ust.marked:
                        b.mark(ust)
                        # check constraints for all tiles adjacent to new marking
                        check_tiles.update(b.get_adjacent(ust))

            if show:
                print(b)
                if (input('press enter to see next move, or q to quit') == 'q'):
                    break

        return probability_of_success

    def complexGAC_max_c(self, b, show):
        ''' same as complexGAC, except heuristic for guessing next tiles (in
            case there's no safe tiles) is maximizing constraints that will be
            checked instead of probability'''
        probability_of_success = 1
        safe_tiles = set()
        first = True
        all_tiles = b.get_all_tiles()

        while not b.solved():

            max_adjacent = 0
            tile = None
            if first:
                tile = b.first_tile_to_pick()
                first = False
            elif len(safe_tiles) > 0:
                # if there's a safe tile, select that one next
                tile = safe_tiles.pop()
                if tile.known:
                    continue
            else:
                # otherwise pick the tile with the most known adjacent tiles
                # find the max number of adjacent tiles
                for t in all_tiles:
                    if t.known or t.marked:
                        continue
                    count = 0
                    current_adj = b.get_adjacent(t)
                    for adj_tile in current_adj:
                        if adj_tile.known and not adj_tile.is_mine:
                            count += 1
                    if count >= max_adjacent:
                        max_adjacent = count
                        tile = t

                #calculate the probability of success
                if tile.minep != 2:
                    probability_of_success *= (1-tile.minep)
                else:
                    base_probability = ((b.number_mines-b.known_mines)/b.unknown_tiles)
                    probability_of_success *= (1-base_probability)


            uncovered_tiles = set(b.select(tile))

            # get tiles to check constraints on
            check_tiles = set()
            check_tiles.update(uncovered_tiles)
            for ut in uncovered_tiles:
                check_tiles.update(b.get_adjacent(ut))

            # check constraints
            while check_tiles:
                ct = check_tiles.pop()
                unsafe = set()
                ssafe, sunsafe, sknownp = b.check_simple_constraint(ct)
                csafe, cunsafe, cknownp = b.check_complex_constraint(ct)
                safe_tiles.update(ssafe)
                safe_tiles.update(csafe)
                # mark tiles that are believed to be mines
                unsafe.update(sunsafe)
                unsafe.update(cunsafe)
                for ust in unsafe:
                    if not ust.marked:
                        b.mark(ust)
                        # check constraints for all tiles adjacent to new marking
                        check_tiles.update(b.get_adjacent(ust))

            if show:
                print(b)
                if (input('press enter to see next move, or q to quit') == 'q'):
                    break

        return probability_of_success

    def human(self, b, show):
        status = 1
        while not b.solved():
            loc = []
            q = False
            while len(loc) < 2:
                loc = input("Please enter a 0-indexed location or q to quit. (row,col): ")
                if loc[0].lower() == 'q' or loc[0].lower() == 'quit':
                    q = True
                    print("QUITTING GAME")
                    status = 0
                    break
            if q:
                break
            print("You have uncovered the tile at position (" + str(loc) + ")")
            loc = loc.split(',')
            tile = b.get_tile(int(loc[0]), int(loc[1]))
            if len(loc) > 2:
                b.mark(tile)
            else:
                # the function to update pmine has not been added yet
                uncovered_tiles = b.select(tile)
                if tile.is_mine:
                    status = -1
                    print("GAME OVER")
                    break

            print(b)

        if status == 1:
            print("CONGRATULATIONS")
        return 1

