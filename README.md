# Minesweeper

### Usage ###
`python test.py <mode>`

### Modes ###

There are 3 modes, "human", "single_test", "full_test". If no mode is provided, it will default to single_test.

-human: Will let a human play the implemented game. Will lose on mine hit. Prints board after every turn. Input to select tile is "row,col". Input to mark tile is "row,col,x"  
-single_test: Will run complex GAC and show the board after every turn. Press enter to see next move, or 'q' to quit. Will not lose on mine hit. Prints number of mines hit and probability of success after completion. To change algorithm, you have to change code (see comments in main, easy to do)  
-full_test: Will run a 1000 iterations of each function and place the output into csv files.  
