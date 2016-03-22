import Board

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

        loc = loc.split(',')
        mark = None if len(loc) == 2 else True
        pmine = b.select(int(loc[0]), int(loc[1]), mark)
        print(b)
        print(b.unknown_tiles)
##        if pmine > 0:
##            if pmine == 2:
##                pmine = (1-b.number_mines+b.known_mines)/(b.unknown_tiles+1)
##            probability_of_success *= pmine
##            print("SUCCCES PROBABILITY DROPPED TO: ",probability_of_success)
    else:
        print("CONGRATULATIONS")


if __name__ == '__main__':
    main()
