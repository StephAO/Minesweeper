import MineSweeperCSP
import Board
import sys
import csv

NUMBER_OF_TEST = 1000
BOARD_SIZES = {
    "beginner" : (9,9,10),
    #"intermediate" : (16,16,40),
    #"expert" : (16,30,99),
    #"custom" : (50,50,500)
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
        """
        bs = BOARD_SIZES["expert"]
        if len(sys.argv) >= 3 and sys.argv[2] in BOARD_SIZES:
            bs = BOARD_SIZES[argv[2]]
        board = Board.Board(bs[0], bs[1], bs[2])
        """
        play.run(play.human, board)

    elif mode == "single_test":
        pass

    elif mode == "full_test":
        test()

def test():
    for difficulty, board_size in BOARD_SIZES.items():
        print(difficulty)
        mine_count = open("mines_hit_"+difficulty+".csv", 'w', newline='')
        prob_succ = open("probability_success_"+difficulty+".csv", 'w', newline='')
        time_taken = open("time_taken_"+difficulty+".csv", 'w', newline='')
        mc_writer = csv.writer(mine_count, quoting=csv.QUOTE_MINIMAL)
        ps_writer = csv.writer(prob_succ,  quoting=csv.QUOTE_MINIMAL)
        tt_writer = csv.writer(time_taken,  quoting=csv.QUOTE_MINIMAL)

        mc_writer.writerow(["simpleFC","simpleGAC","complexFC","complexGAC"])
        ps_writer.writerow(["simpleFC","simpleGAC","complexFC","complexGAC"])
        tt_writer.writerow(["simpleFC","simpleGAC","complexFC","complexGAC"])

        for i in range(NUMBER_OF_TEST):
            if (i%100 == 0):
                print(i)
            b = Board.Board(board_size[0], board_size[1], board_size[2])
            solve = MineSweeperCSP.MineSweeperCSP()
            solve.run_all(b,mc_writer, ps_writer, tt_writer)

        mine_count.close()
        prob_succ.close()
        time_taken.close()

if __name__ == '__main__':

    main()
