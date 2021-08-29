import math
from copy import deepcopy
from pprint import pprint
import os
import timeit
import random
import sys
is_windows = sys.platform.startswith('win')
def clear():
  if is_windows:
    os.system('cls')
  else:
    os.system('clear')
blank = [[2,8,0,0,0,0,0,0,1],
         [0,0,0,8,0,1,0,0,4],
         [0,0,4,0,7,0,3,0,0],
         [0,2,0,0,5,0,0,6,0],
         [0,0,3,1,0,9,7,0,0],
         [0,1,0,0,8,0,0,5,0],
         [0,0,1,0,6,0,8,0,0],
         [5,0,0,2,0,3,0,0,0],
         [9,0,0,0,0,0,0,1,6]]

class Board:
  def __init__(self, board):
    self.board = deepcopy(board)
    self.backup = deepcopy(board)
  def getBoard(self):
    return self.board
  def getBackup(self):
    return self.backup
  def setBackup(self, board):
    self.backup = deepcopy(board)
  def restoreBackup(self):
    self.board = deepcopy(self.backup)
  def isSolved(self):
    result = {'solved': True}
    flippedBoard = []
    for i in range(0,9):
      flippedBoard.append([])
    blockBoard = []
    for i in range(0,9):
      blockBoard.append([])

    for row, rowArray in enumerate(self.board):
      numberFrequency = {}
      for col, value in enumerate(rowArray):
          blockBoard[math.floor(col/3)+(math.floor(row/3) * 3)].append(value)
          flippedBoard[col].append(value)
          if value in numberFrequency:
            numberFrequency[value] += 1
          elif value != 0:
            numberFrequency[value] = 1
      for number, count in numberFrequency.items():
        if count > 1:
          result = {"solved": False, "error": "duplicate_in_row"}
    for row, rowArray in enumerate(blockBoard):
      numberFrequency = {}
      for col, value in enumerate(rowArray):
          if value in numberFrequency:
            numberFrequency[value] += 1
          elif value != 0:
            numberFrequency[value] = 1
      for number, count in numberFrequency.items():
        if count > 1:
          result = {"solved": False, "error": "duplicate_in_blocks"}
    for row, rowArray in enumerate(flippedBoard):
      numberFrequency = {}
      for col, value in enumerate(rowArray):
          if value in numberFrequency:
            numberFrequency[value] += 1
          elif value != 0:
            numberFrequency[value] = 1
      for number, count in numberFrequency.items():
        if count > 1:
          result = {"solved": False, "error": "duplicate_in_col"}

      for column in rowArray:
        if column == 0:
          result = {"solved": False, "error": "empty_space"}
    return result
  def hasErrors(self, testArray):
    result = {'errors': False}
    flippedBoard = []
    for i in range(0,9):
      flippedBoard.append([])
    blockBoard = []
    for i in range(0,9):
      blockBoard.append([])

    for row, rowArray in enumerate(testArray):
      numberFrequency = {}
      for col, value in enumerate(rowArray):
          blockBoard[math.floor(col/3)+(math.floor(row/3) * 3)].append(value)
          flippedBoard[col].append(value)
          if value in numberFrequency:
            numberFrequency[value] += 1
          elif value != 0:
            numberFrequency[value] = 1
      for number, count in numberFrequency.items():
        if count > 1:
          result = {"errors": True, "error": "duplicate_in_row"}
    for row, rowArray in enumerate(blockBoard):
      numberFrequency = {}
      for col, value in enumerate(rowArray):
          if value in numberFrequency:
            numberFrequency[value] += 1
          elif value != 0:
            numberFrequency[value] = 1
      for number, count in numberFrequency.items():
        if count > 1:
          result = {"errors": True, "error": "duplicate_in_blocks"}
    for row, rowArray in enumerate(flippedBoard):
      numberFrequency = {}
      for col, value in enumerate(rowArray):
          if value in numberFrequency:
            numberFrequency[value] += 1
          elif value != 0:
            numberFrequency[value] = 1
      for number, count in numberFrequency.items():
        if count > 1:
          result = {"errors": True, "error": "duplicate_in_col"}
    return result
  def placeNumber(self, row, column, value):
    oldBoard = deepcopy(self.board)
    targetRow = oldBoard[row]
    for n, i in enumerate(targetRow):
      if n == column:
        targetRow[n] = value
    newBoard = oldBoard
    newBoard[row] = targetRow

    if self.hasErrors(newBoard)['errors'] == False:
      self.board = deepcopy(newBoard)
      return {"errors": False, 'board': newBoard};
    else:
      return {"errors": True, "error": "illegal_placement"};
  def canPlace(self, row, column, value):
    oldBoard = deepcopy(self.board)
    targetRow = oldBoard[row]
    for n, i in enumerate(targetRow):
      if n == column:
        targetRow[n] = value
    newBoard = oldBoard
    newBoard[row] = targetRow

    if self.hasErrors(newBoard)['errors'] == False:
      return {"errors": False, 'board': newBoard};
    else:
      return {"errors": True, "error": "illegal_placement"};
  def positionValue(self, row, column):
    oldBoard = deepcopy(self.board)
    targetRow = oldBoard[row]
    for n, i in enumerate(targetRow):
      if n == column:
        return i;
        break;

sudoku = Board(blank)

clear()
pprint(sudoku.getBoard())

start = timeit.default_timer()

# Find all 0's and then get possibilities for each square and fill in rows with only 1 possibility until there's no more singular possibility slots.
def fillInSingularPossibilities(soduku, n):
  potentialBoardValues = []
  for i in range(0,9):
    potentialBoardValues.append([])
    for position in range(0,9):
      if sudoku.positionValue(i, position) != 0:
        potentialBoardValues[i].append(sudoku.positionValue(i, position))
      else:
        potentialBoardValues[i].append([])

  hasSingular = False
  invalidBoard = False
  for row, rowArray in enumerate(sudoku.board):
    for col, value in enumerate(rowArray):
      if value == 0:
        for potential in range(1,10):
          if sudoku.canPlace(row, col, potential)['errors'] == False:
            potentialBoardValues[row][col].append(potential)
        if len(potentialBoardValues[row][col]) == 0:
          invalidBoard = True
        if len(potentialBoardValues[row][col]) == 1:
          hasSingular = True
          sudoku.placeNumber(row, col, potentialBoardValues[row][col][0])
          clear()
          pprint(sudoku.getBoard());

  if invalidBoard:
    invalidBoard = False
    soduku.restoreBackup()
    fillInSingularPossibilities(sudoku, 0)
  if hasSingular:
    hasSingular = False
    fillInSingularPossibilities(sudoku, 0)
  else:
    if soduku.isSolved()['solved']:
      clear()
      stop = timeit.default_timer()
      print("Solved soduku board in", stop-start, "seconds.")
      pprint(soduku.getBoard())
      quit()
    else:
      if n != 0:
        soduku.restoreBackup()
        fillInSingularPossibilities(sudoku, 1)
      else:
        for row, rowArray in enumerate(potentialBoardValues):
          for col, value in enumerate(rowArray):
            if not isinstance(value, int):
              soduku.placeNumber(row, col, random.choice(value))
              fillInSingularPossibilities(sudoku, 1)
                


fillInSingularPossibilities(sudoku, 0)