import MineSweeperCSP
import Board
import sys
import csv

NUMBER_OF_TEST = 1000

def add(a):
    a.append(5)

def main():
    mode = "complexGAC"
    if len(sys.argv) == 2:
        mode = sys.argv[1]

    mine_count = open('mineData.csv', 'w', newline='')
    prob_succ = open('probData.csv', 'w', newline='')
    mc_writer = csv.writer(mine_count, quoting=csv.QUOTE_MINIMAL)
    ps_writer = csv.writer(prob_succ,  quoting=csv.QUOTE_MINIMAL)
    for i in range(NUMBER_OF_TEST):

        b = Board.Board(16,30,99) # [(1,1),(2,2),(3,4),(2,4)]
        solve = MineSweeperCSP.MineSweeperCSP()
        solve.set_mode(mode)
        solve.run_all(b,mc_writer, ps_writer)

    mine_count.close()
    prob_succ.close()

if __name__ == '__main__':
    main()
