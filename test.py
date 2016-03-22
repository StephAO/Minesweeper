import Board

def add(a):
    a.append(5)

def main():
    b = Board.Board(6,6) # [(1,1),(2,2),(3,4),(2,4)]
    while not b.solved():
        loc = input("Please enter a 0-indexed location. (row,col): ")
        print(loc)
        loc = loc.split(',')
        flag = False
        minefree = b.select(int(loc[0]), int(loc[1]), len(loc) > 2 and loc[2]=='f')
        print(b)
        if not minefree:
            break
    else:
        print("CONGRATULATIONS")


if __name__ == '__main__':
    main()
