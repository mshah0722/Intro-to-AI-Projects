import queue
import heapq
import sys
import time
import argparse
import copy
from queue import PriorityQueue
from turtle import st

# Global variables for max rows and columns
rows = 5
columns = 4

# Main class to store the state 
class State:
    
    # Initialize the object's attributes 
    def __init__(self):
        self.parent = None
        self.pathCostVal = 0
        self.heuristicVal = 0
        self.aStarVal = 0
        self.board = []
        self.availablePosition = [(0,0), (0,0)]
        self.prevMove = -1, "None"

    # Process the initial board configuration file
    def process_input(self, file):
        openFile = open(file, 'r')
        allLines = openFile.readlines()
        
        currRow = 0
        currColumn = 0
        emptySpaceCount = 0
        cols = []
        
        # Iterate through the lines and store the board configuration in self.board
        for line in allLines:
            for i in range(columns):
                intValue = int(line[i])
                cols.append(intValue)
                
                # If the value is zero, then store the position of the empty position in self.available position
                if intValue == 0:
                    self.availablePosition[emptySpaceCount] = (currRow, currColumn)
                    emptySpaceCount += 1
                currColumn += 1
                
            self.board.append(cols)
            cols = []
            currColumn = 0
            currRow += 1

    # Set the current state to parent state
    def set_current_state_to_parent_state(self, otherState):
        # Make the current state's parent be the the parent state
        self.parent = otherState
        
        # Make the current board be the same as the parent board
        self.board = otherState.board

        self.availablePosition[0] = otherState.availablePosition[0]
        self.availablePosition[1] = otherState.availablePosition[1]

        # Increase the cost to the current path by 1
        self.pathCostVal = otherState.pathCostVal + 1
        

    # find the position relative to a piece
    # input: position of a piece, direction (left,right,up,down)
    # output: the position of the neighboring piece (row,col)
    def find_position(self, pos, direction):
        if direction == "left":
            row = pos[0]
            col = pos[1] - 1
        elif direction == "right":
            row = pos[0]
            col = pos[1] + 1
        elif direction == "up":
            row = pos[0] - 1
            col = pos[1]
        elif direction == "down":
            row = pos[0] + 1
            col = pos[1]
        else:
            (col, row) = (-1, -1)
        return row, col



    # move a piece to the available position
    # input: space, which space to move, direction (left,right,up,down)
    # output: newState, after the move
    def move(self, space, direction):
        newState = State()
        newState.set_current_state_to_parent_state(self)  # create a child state by copying from the info of its parent,
        # we will modify the child's info later

        row1, col1 = self.availablePosition[0]
        row2, col2 = self.availablePosition[1]

        pos = self.availablePosition[space]
        r, c = pos
        (row, col) = self.find_position(pos, direction)
        piece = int(self.board[row][col])

        if piece == 1:
            if direction == "left":
                newState.board[row1][col1 - 2] = 0
                newState.board[row2][col2 - 2] = 0
                newState.availablePosition = [(row1, col1 - 2), (row2, col2 - 2)]
            elif direction == "right":
                newState.board[row1][col1 + 2] = 0
                newState.board[row2][col2 + 2] = 0
                newState.availablePosition = [(row1, col1 + 2), (row2, col2 + 2)]
            elif direction == "up":
                newState.board[row1 - 2][col1] = 0
                newState.board[row2 - 2][col2] = 0
                newState.availablePosition = [(row1 - 2, col1), (row2 - 2, col2)]
            elif direction == "down":
                newState.board[row1 + 2][col1] = 0
                newState.board[row2 + 2][col2] = 0
                newState.availablePosition = [(row1 + 2, col1), (row2 + 2, col2)]

            newState.board[row1][col1] = 1
            newState.board[row2][col2] = 1

        elif piece == 7:
            newState.board[r][c] = 7
            newState.availablePosition[space] = (row, col)
            newState.board[row][col] = 0
        elif 2 <= piece <= 6:
            if direction == "left":
                if c - 2 >= 0 and newState.board[r][c - 2] == piece:
                    # horizontal
                    newState.board[r][c] = piece
                    newState.board[r][c - 2] = 0
                    newState.availablePosition[space] = (r, c - 2)
                else:
                    # vertical
                    newState.board[row1][col1 - 1] = 0
                    newState.board[row2][col2 - 1] = 0
                    newState.board[row1][col1] = piece
                    newState.board[row2][col2] = piece
                    newState.availablePosition = [(row1, col1 - 1), (row2, col2 - 1)]

            elif direction == "right":
                if c + 2 < columns and newState.board[r][c + 2] == piece:
                    # horizontal
                    newState.board[r][c] = piece
                    newState.board[r][c + 2] = 0
                    newState.availablePosition[space] = (r, c + 2)
                else:
                    # vertical
                    newState.board[row1][col1 + 1] = 0
                    newState.board[row2][col2 + 1] = 0
                    newState.board[row1][col1] = piece
                    newState.board[row2][col2] = piece
                    newState.availablePosition = [(row1, col1 + 1), (row2, col2 + 1)]

            elif direction == "up":
                if r - 2 >= 0 and newState.board[r - 2][c] == piece:
                    # vertical
                    newState.board[r - 2][c] = 0
                    newState.board[r][c] = piece
                    newState.availablePosition[space] = (r - 2, c)
                else:  # horizontal
                    newState.board[row1][col1] = piece
                    newState.board[row2][col2] = piece
                    newState.board[row1 - 1][col1] = 0
                    newState.board[row2 - 1][col2] = 0
                    newState.availablePosition = [(row1 - 1, col1), (row2 - 1, col2)]

            elif direction == "down":
                if r + 2 < rows and newState.board[r + 2][c] == piece:
                    # vertical
                    newState.board[r + 2][c] = 0
                    newState.board[r][c] = piece
                    newState.availablePosition[space] = (r + 2, c)
                else:  # horizontal
                    newState.board[row1][col1] = piece
                    newState.board[row2][col2] = piece
                    newState.board[row1 + 1][col1] = 0
                    newState.board[row2 + 1][col2] = 0
                    newState.availablePosition = [(row1 + 1, col1), (row2 + 1, col2)]
        newState.heuristicVal = get_a_star_val(newState)
        newState.prevMove = (space, direction)
        return newState

    def __str__(self):
        bb = ""
        for i in range(rows):
            line = ""
            for j in range(columns):
                line += str(self.board[i][j])
            bb += line + "\n"
        return bb

    # override the equal operator
    def __eq__(self, otherState):
        if self.board == otherState.board:
            return True
        else:
            return False

    # override the comparison operator <
    def __lt__(self, otherState):
        return self.aStarVal < otherState.aStarVal

# Returns the string of a board configuration to store in the explored states    
def convert_board_to_string(board):
    temp = [ y for x in board for y in x]
    boardString = ','.join(map(str,temp))
    return boardString

# Return a list of all successor states
def get_successor_states(currState, exploredStates):
    allSuccessorsStates = []

    space1 = currState.availablePosition[0]
    space2 = currState.availablePosition[1]

    row = space1[0]
    col = space1[1]
    space = 0

    flag = False

    direction = "right"
    if col != 3 and currState.prevMove != (space, "left"):
        piece = currState.board[row][col + 1]
        if piece == 1:
            if space2 == (row + 1, col) and currState.board[row + 1][col + 1] == 1:
                flag = True
            elif space2 == (row - 1, col) and currState.board[row - 1][col + 1] == 1:
                flag = True
        elif piece == 7:
            flag = True
        elif 2 <= piece <= 6:
            if col + 2 < columns and currState.board[row][col + 2] == piece:  # horizontal
                flag = True
            elif space2 == (row + 1, col) and currState.board[row + 1][col + 1] == piece:
                flag = True
            elif space2 == (row - 1, col) and currState.board[row - 1][col + 1] == piece:
                flag = True

    if flag:
        newState = currState.move(space, direction)
        if convert_board_to_string(newState.board) not in exploredStates:
            allSuccessorsStates.append(newState)
    flag = False

    direction = "left"

    if col != 0 and currState.prevMove != (space, "right"):
        piece = currState.board[row][col - 1]
        if piece == 1:
            if space2 == (row - 1, col) and currState.board[row - 1][col - 1] == 1:
                flag = True
            elif space2 == (row + 1, col) and currState.board[row + 1][col - 1] == 1:
                flag = True
        elif piece == 7:
            flag = True
        elif 2 <= piece <= 6:
            if col - 2 >= 0 and currState.board[row][col - 2] == piece:  # horizontal
                flag = True
            elif space2 == (row + 1, col) and currState.board[row + 1][col - 1] == piece:
                flag = True
            elif space2 == (row - 1, col) and currState.board[row - 1][col - 1] == piece:
                flag = True
    if flag:
        newState = currState.move(space, direction)
        if convert_board_to_string(newState.board) not in exploredStates:
            allSuccessorsStates.append(newState)
    flag = False

    direction = "up"
    if row != 0 and currState.prevMove != (space, "down"):
        piece = currState.board[row - 1][col]
        if piece == 1:
            if space2 == (row, col + 1) and currState.board[row - 1][col + 1] == 1:
                flag = True
            elif space2 == (row, col - 1) and currState.board[row - 1][col - 1] == 1:
                flag = True
        elif piece == 7:
            flag = True
        elif 2 <= piece <= 6:
            # print("piece2-6")
            if row - 2 >= 0 and currState.board[row - 2][col] == piece:  # vertical
                flag = True
            elif space2 == (row, col + 1) and currState.board[row - 1][col + 1] == piece:
                flag = True
            elif space2 == (row, col - 1) and currState.board[row - 1][col - 1] == piece:
                flag = True
    if flag:
        newState = currState.move(space, direction)
        if convert_board_to_string(newState.board) not in exploredStates:
            allSuccessorsStates.append(newState)
    flag = False

    direction = "down"
    if row != columns and currState.prevMove != (space, "up"):
        piece = currState.board[row + 1][col]
        if piece == 1:
            if space2 == (row, col + 1) and currState.board[row + 1][col + 1] == 1:
                flag = True
            elif space2 == (row, col - 1) and currState.board[row + 1][col - 1] == 1:
                flag = True
        elif piece == 7:
            flag = True
        elif 2 <= piece <= 6:
            if row + 2 < rows and currState.board[row + 2][col] == piece:  # vertical
                flag = True
            elif space2 == (row, col + 1) and currState.board[row + 1][col + 1] == piece:
                flag = True
            elif space2 == (row, col - 1) and currState.board[row + 1][col - 1] == piece:
                flag = True
    if flag:
        newState = currState.move(space, direction)
        if convert_board_to_string(newState.board) not in exploredStates:
            allSuccessorsStates.append(newState)
    flag = False

    row = space2[0]
    col = space2[1]
    space = 1
    # left of space2
    direction = "left"
    if col != 0 and currState.prevMove != (space, "right"):
        piece = currState.board[row][col - 1]
        if piece == 7:
            flag = True
        elif 2 <= piece <= 6:
            if col - 2 >= 0:  # horizontal piece
                if currState.board[row][col - 2] == piece:
                    flag = True
    if flag:
        newState = currState.move(space, direction)
        if convert_board_to_string(newState.board) not in exploredStates:
            allSuccessorsStates.append(newState)
    flag = False

    direction = "right"
    if col != 3 and currState.prevMove != (space, "left"):
        piece = currState.board[row][col + 1]
        if piece == 7:
            flag = True
        elif 2 <= piece <= 6:
            if col + 2 < columns and currState.board[row][col + 2] == piece:  # horizontal piece
                flag = True
    if flag:
        newState = currState.move(space, direction)
        if convert_board_to_string(newState.board) not in exploredStates:
            allSuccessorsStates.append(newState)
    flag = False

    direction = "down"
    if row != columns and currState.prevMove != (1, "up"):
        piece = currState.board[row + 1][col]
        if piece == 7:
            flag = True
        elif 2 <= piece <= 6:
            if row + 2 < rows and currState.board[row + 2][col] == piece:  # vertical piece
                flag = True
    if flag:
        newState = currState.move(space, direction)
        if convert_board_to_string(newState.board) not in exploredStates:
            allSuccessorsStates.append(newState)
    flag = False

    direction = "up"
    if row != 0 and currState.prevMove != (1, "down"):
        piece = currState.board[row - 1][col]
        if piece == 7:
            flag = True
        elif 2 <= piece <= 6:
            if row - 2 >= 0 and currState.board[row - 2][col] == piece:  # vertical piece
                flag = True
    if flag:
        newState = currState.move(space, direction)
        if convert_board_to_string(newState.board) not in exploredStates:
            allSuccessorsStates.append(newState)
    '''
    print("\nallSuccessorsStates:")
    for i in allSuccessorsStates:
        print(i)
        print("") '''

    return allSuccessorsStates

# Return cost to the current state
def get_path_cost_val(state):
    return state.pathCostVal

# Return the Manhattan distance heuristic from current state to goal state
def get_heuristic_val(state):   
    for i in range(rows):
        for j in range(columns):
            if state.board[i][j] == 1:
                # The Manhattan distance between the 2x2 piece and the bottom opening
                state.heuristicVal = abs(i - 3) + abs(j - 1)
                return state.heuristicVal

# Return A* Priority of the state
def get_a_star_val(state):
    state.aStarVal = get_heuristic_val(state) + get_path_cost_val(state)
    return state.aStarVal

# Check whether Current State is the Goal State
def is_goal_state(currState):
    if currState.board[3][1] == 1 and currState.board[3][2] == 1 and currState.board[4][1] == 1 and currState.board[4][2] == 1:
        return True
    return False

# Solve using Depth First Search and return the path to the solution
def dfs_agorithm(startingState):
    # Store all the explored states in a set
    exploredStates = set()
    
    # Store the frontier in a LIFO stack
    frontier = queue.LifoQueue()
    frontier.put(startingState)
    
    boardString = convert_board_to_string(startingState.board)
    exploredStates.add(boardString)

    while frontier:
        currState = frontier.get()
        allSuccessorsStates = get_successor_states(currState, exploredStates)

        for successorState in allSuccessorsStates:
            if is_goal_state(successorState):
                # If it is the goal state, follow the path to the starting state
                pathToCurrentState = []
                while successorState != startingState:
                    pathToCurrentState.insert(0, successorState)
                    successorState = successorState.parent
                pathToCurrentState.insert(0, startingState)
                return pathToCurrentState
            boardString = convert_board_to_string(successorState.board)
            exploredStates.add(boardString)
            
            frontier.put(successorState)
    # If no solution is found, return None
    return None


# Solve using A* Algorithm with Manhattan distance heuristic and return the path to the solution
def a_star_algorithm(startingState):
    # Store all the explored states in a set
    exploredStates = set()
    
    # Store the frontier as a Priority Queue of the state's A* Value
    frontier = PriorityQueue()
    frontier.put((get_a_star_val(startingState), startingState))
    
    boardString = convert_board_to_string(startingState.board)
    exploredStates.add(boardString)

    while frontier:
        currState = frontier.get()[1]
        allSuccessorsStates = get_successor_states(currState, exploredStates)

        for successorState in allSuccessorsStates:
            if is_goal_state(successorState):
                # If it is the goal state, follow the path to the starting state
                pathToCurrentState = []
                while successorState != startingState:
                    pathToCurrentState.insert(0, successorState)
                    successorState = successorState.parent
                pathToCurrentState.insert(0, startingState)
                return pathToCurrentState
            boardString = convert_board_to_string(successorState.board)
            exploredStates.add(boardString)
            frontier.put((get_a_star_val(successorState), successorState))
    # If no solution is found, return None
    return None

def process_output(puzzleID, outputFile1, outputFile2):
    dfsState = State()
    aStarState = State()
    
    dfsState.process_input(puzzleID)
    aStarState.process_input(puzzleID)
    
    pathToCurrentState1 = dfs_agorithm(dfsState)
    pathToCurrentState2 = a_star_algorithm(aStarState)

    # Write the output for DFS Solution first
    f = open(outputFile1, "w")
    
    f.write("Cost of the solution: " + str(pathToCurrentState1[-1].pathCostVal) + "\n")
    
    for state in pathToCurrentState1:
        for row in state.board:
            for col in row:
                f.write(str(col))
            f.write("\n")
        f.write("\n")
  
    f.close()
    
    # Write the output for A* Solution next
    f = open(outputFile1, "w")
    
    f.write("Cost of the solution: " + str(pathToCurrentState2[-1].pathCostVal) + "\n")
    
    for state in pathToCurrentState1:
        for row in state.board:
            for col in row:
                f.write(str(col))
            f.write("\n")
        f.write("\n")
  
    f.close()

if __name__ == "__main__":
    puzzleID = sys.argv[1]
    outputFile1 = sys.argv[2]
    outputFile2 = sys.argv[3]
    process_output(puzzleID, outputFile1, outputFile2)