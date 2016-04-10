import MineSweeperCSP
import Board
import sys
import csv

NUMBER_OF_TEST = 2
BOARD_SIZES = {
    "beginner" : (9,9,10),
    "intermediate" : (16,16,40),
    "expert" : (16,30,99),
    "custom" : (50,50,500)
}

def add(a):
    a.append(5)

def main():
    mode = "full_test"
    if len(sys.argv) >= 2:
        mode = sys.argv[1]

    if mode == "human":

        row = input("Enter a row size: ")
        column = input("Enter a column size: ")
        while True:
            mines = input("Do you want the assign the number of mines? (y, n): ")
            if mines == 'n' or mines == 'y':
                break
        if mines == "y":
            num_mines = input("How many mines?: ")
            if int(num_mines) > (int(row) * int(column)):
                num_mines = (int(row) * int(column))
            board = Board.Board(int(column), int(row), int(num_mines))
        if mines == "n":
            board = Board.Board(int(column), int(row))

        play = MineSweeperCSP.MineSweeperCSP()
        play.run(play.human, board)

    elif mode == "single_test":
        ''' run single test, change settings in code
            To see the moves taken by the algorithm add the following lines
            add the bottom of the for loop in any of the algorithms in MineSweeperCSP:

            # don't add this (just to see format)
            while not b.solved():
                .
                .
                .
            # add this
                print(b)
                if (input('press enter to see next more, or q to quit') == 'q'):
                    break
        '''
        solve = MineSweeperCSP.MineSweeperCSP()
        solve.run(solve.complexGAC, Board.Board(9,9,10))

    elif mode == "full_test":
        ''' Will test every function defined in the list created on
            MineSweeperCSP constructor'''
        test()

def test():
    for difficulty, board_size in BOARD_SIZES.items():
        print(difficulty)
        mine_count = open("h_mines_hit_"+difficulty+".csv", 'w', newline='')
        prob_succ = open("h_probability_success_"+difficulty+".csv", 'w', newline='')
        time_taken = open("h_time_taken_"+difficulty+".csv", 'w', newline='')
        mc_writer = csv.writer(mine_count, quoting=csv.QUOTE_MINIMAL)
        ps_writer = csv.writer(prob_succ,  quoting=csv.QUOTE_MINIMAL)
        tt_writer = csv.writer(time_taken,  quoting=csv.QUOTE_MINIMAL)

        mc_writer.writerow(["minize_probability", "maximize_constraints"])
        ps_writer.writerow(["minize_probability", "maximize_constraints"])
        tt_writer.writerow(["minize_probability", "maximize_constraints"])

        for i in range(NUMBER_OF_TEST):
##            if ((i+1)%int(NUMBER_OF_TEST/10) == 0):
##                print(str(((i+1)/int(NUMBER_OF_TEST/10))*10)+"%")
            b = Board.Board(board_size[0], board_size[1], board_size[2])
            solve = MineSweeperCSP.MineSweeperCSP()
            solve.run_all(b,mc_writer, ps_writer, tt_writer)

        mine_count.close()
        prob_succ.close()
        time_taken.close()

if __name__ == '__main__':

    main()
