import MineSweeperCSP
import Board
import sys

def add(a):
    a.append(5)

def main():
    mode = "complexGAC"
    if len(sys.argv) == 2:
        mode = sys.argv[1]
    b = Board.Board(16,30,99) # [(1,1),(2,2),(3,4),(2,4)]
    solve = MineSweeperCSP.MineSweeperCSP()
    solve.set_mode(mode)
    solve.run_all(b)

if __name__ == '__main__':
    main()
