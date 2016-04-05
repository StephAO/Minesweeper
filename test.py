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

    # Beginner
    mine_count = open('mineDataBeginner.csv', 'w', newline='')
    prob_succ = open('probDataBeginner.csv', 'w', newline='')
    mc_writer = csv.writer(mine_count, quoting=csv.QUOTE_MINIMAL)
    ps_writer = csv.writer(prob_succ,  quoting=csv.QUOTE_MINIMAL)
    for i in range(NUMBER_OF_TEST):

        b = Board.Board(9,9,10)
        solve = MineSweeperCSP.MineSweeperCSP()
        solve.set_mode(mode)
        solve.run_all(b,mc_writer, ps_writer)

    mine_count.close()
    prob_succ.close()

    # Intermediate
    mine_count = open('mineDataIntermediate.csv', 'w', newline='')
    prob_succ = open('probDataIntermediate.csv', 'w', newline='')
    mc_writer = csv.writer(mine_count, quoting=csv.QUOTE_MINIMAL)
    ps_writer = csv.writer(prob_succ,  quoting=csv.QUOTE_MINIMAL)
    for i in range(NUMBER_OF_TEST):

        b = Board.Board(16,16,40)
        solve = MineSweeperCSP.MineSweeperCSP()
        solve.set_mode(mode)
        solve.run_all(b,mc_writer, ps_writer)

    mine_count.close()
    prob_succ.close()

    # Expert
    mine_count = open('mineDataExpert.csv', 'w', newline='')
    prob_succ = open('probDataExper.csv', 'w', newline='')
    mc_writer = csv.writer(mine_count, quoting=csv.QUOTE_MINIMAL)
    ps_writer = csv.writer(prob_succ,  quoting=csv.QUOTE_MINIMAL)
    for i in range(NUMBER_OF_TEST):

        b = Board.Board(16,30,99)
        solve = MineSweeperCSP.MineSweeperCSP()
        solve.set_mode(mode)
        solve.run_all(b,mc_writer, ps_writer)

    mine_count.close()
    prob_succ.close()

    # Custom
    mine_count = open('mineDataCustom.csv', 'w', newline='')
    prob_succ = open('probDataCustom.csv', 'w', newline='')
    mc_writer = csv.writer(mine_count, quoting=csv.QUOTE_MINIMAL)
    ps_writer = csv.writer(prob_succ,  quoting=csv.QUOTE_MINIMAL)
    for i in range(NUMBER_OF_TEST):

        b = Board.Board(50,50,500)
        solve = MineSweeperCSP.MineSweeperCSP()
        solve.set_mode(mode)
        solve.run_all(b,mc_writer, ps_writer)

    mine_count.close()
    prob_succ.close()

if __name__ == '__main__':
    main()
