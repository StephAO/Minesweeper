import Board

def add(a):
    a.append(5)

def main():
    b = Board.Board(6,6) # [(1,1),(2,2),(3,4),(2,4)]
    while not b.solved():
        loc = input("Please enter a 0-indexed location. (row,col): ")
        loc = [int(i) for i in loc.split(',')]
        minefree = b.select(loc[0], loc[1])
        print(b)
        if not minefree:
            break
    else:
        print("CONGRATULATIONS")


if __name__ == '__main__':
    main()
