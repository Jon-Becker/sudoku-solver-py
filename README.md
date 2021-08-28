# sudoku-solver-py
soduku-solver-py is a simple program I challenged myself to create in 6 hours in python. Python is a language I need the most practice with, so I felt like this would be a good project to challenge that. This was a timed challenge, so there are most likely bugs, and it is not efficient at all.

## How it works
- An object `Board` is generated which contains `self.board` and `self.backup`, with various helper classes such as `Board.restoreBackup()` and `Board.canPlaceNumber`.
- The `self.board` object is an array of 9 1 x 9 arrays, for example:
  ```
   [[2,8,0,0,0,0,0,0,1],
   [0,0,0,8,0,1,0,0,4],
   [0,0,4,0,7,0,3,0,0],
   [0,2,0,0,5,0,0,6,0],
   [0,0,3,1,0,9,7,0,0],
   [0,1,0,0,8,0,0,5,0],
   [0,0,1,0,6,0,8,0,0],
   [5,0,0,2,0,3,0,0,0],
   [9,0,0,0,0,0,0,1,6]]
   ```
- The program then generates an array `potentialBoardValues`, and assigns each blank space an array with all numbers that could be possible numbers for that space.
- We loop through `potentialBoardValues` and find where only 1 value can be placed there. This action is repeated until there are no more guaranteed values.
- We now recursively loop through `potentialBoardValues	`, assigning numbers and searching for singular possibilities, reverting to a backup board when an invalid board is encountered.
	- At some point the board will be solved, which can take anywhere from 1 second to 1 minute, since its not very efficient at all.

### Todo
If I ever do revisit this project, I need to revamp the correction system so it goes back to the furthest correct point. Right now, we backup to the beginning when encountering an invalid board, which exponentially increases solve times.

### Credits
This project is completely coded by [Jonathan Becker](https://jbecker.dev), using no external libraries.

