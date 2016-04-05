import Board
import Tile
import sys

class MineSweeperCSP:

    def set_mode(self, fn_name):
        if fn_name == "simpleFC":
            self.fn = self.simpleFC
        elif fn_name == "simpleGAC":
            self.fn = self.simpleGAC
        elif fn_name == "complexFC":
            self.fn = self.complexFC
        elif fn_name == "complexGAC":
            self.fn = self.complexGAC
        elif fn_name == "backtrack":
            self.fn == self.backtrack
        elif fn_name == "human":
            self.fn = self.human
        else:
            print("INVALID CSP")
            sys.exit()

    def run(self, board):
        p = self.fn(board)
        print("Probability of success =",str(p*100)+"%","\nMines hit",board.mines_hit,"/",board.number_mines)
        print("-"*30)
        board.reset()

    def run_all(self, board):
        print("Running simpleFC")
        p = self.simpleFC(board)
        print("Probability of success =",str(p*100)+"%","\nMines hit",board.mines_hit,"/",board.number_mines)
        print("-"*30)
        board.reset()
        print("Running simpleGAC")
        p = self.simpleGAC(board)
        print("Probability of success =",str(p*100)+"%","\nMines hit",board.mines_hit,"/",board.number_mines)
        print("-"*30)
        board.reset()
        print("Running complexGAC")
        p = self.complexGAC(board)
        print("Probability of success =",str(p*100)+"%","\nMines hit",board.mines_hit,"/",board.number_mines)
        print("-"*30)
        board.reset()


    def simpleFC(self, b):
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

        return probability_of_success

    def simpleGAC(self, b):
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

        return probability_of_success

    def complexFC(self, b):
        pass

    def complexGAC(self, b):
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
##                    print("picking tile:",tile," with tilep:", 1-tile.minep)
                else:
                    tile = unknown_probabilities.pop()
                    if tile.known:
                        continue
                    probability_of_success *= (1-base_probability)
##                    print("picking tile:",tile," with basep:", 1-base_probability)

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
##            print(b.unknown_tiles)
##            print(safe_tiles)
##            print(b)
##            if input("press Enter") == "q":
##                break

        return probability_of_success

    def backtrack(self, b):
        pass

    def human(self, b):
        status = 1
        while not b.solved():
            loc = []
            q = False
            while len(loc) < 2:
                loc = input("Please enter a 0-indexed location. (row,col): ")
                if loc[0].lower() == 'q' or loc[0].lower() == 'quit':
                    q = True
                    print("QUITTING GAME")
                    status = 0
                    break
            if q:
                break
            print(loc)
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

