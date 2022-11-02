# Global imports
import sys
import copy
from math import inf

# Global variables
rows = 6
rowConstraint = []
columns = 6
columnConstraint = []
ships = {"Submarines": 0, "Destroyers": 0, "Cruisers": 0, "Battleships": 0}

# Main class to store the state 
class State:
    
    # Initialize the object's attributes 
    def __init__(self):
        self.board = []
        self.rowPieceCounter = [0] * rows
        self.columnPieceCounter = [0] * columns
        self.totalPieceCount = 0
        self.totalEmptySpots = 0
        self.submarineCount = 0
        self.destroyerCount = 0
        self.cruiserCount = 0
        self.battleshipCount = 0
        #self.evaluationValue = 0
        #self.gameOver = False
        #self.changeX = [1,1,-1,-1]
        #self.changeY = [1,-1,1,-1]

    # Process the initial board configuration file
    def process_input(self, file):
        openFile = open(file, 'r')
        allLines = openFile.readlines()
        cols = []
        
        # Iterate through the lines and store the board configuration in self.board
        for iter, line in enumerate(allLines):
            if iter == 0:
                global rows 
                rows = len(line) - 1

                for i in range(rows):
                    rowConstraint.append(int(line[i]))
            
            elif iter == 1:
                global columns 
                columns = len(line) - 1

                for i in range(columns):
                    columnConstraint.append(int(line[i]))

            elif iter == 2:
                length = len(line) - 1

                for i in range(length):
                    if i == 0:
                        ships["Submarines"] = int(line[i])
                    elif i == 1:
                        ships["Destroyers"] = int(line[i])
                    elif i == 2:
                        ships["Cruisers"] = int(line[i])
                    elif i == 3:
                        ships["Battleships"] = int(line[i])

            else:
                for i in range(columns):
                    position = line[i]
                    cols.append(position)
                self.board.append(cols)
                cols = []
        return
    
    # Process the output board configuration file
    def process_output(self, file):
        openFile = open(file, 'w')
        
        cols = []
        
        # Iterate through the board and store the board configuration in output file
        for x in range(rows):
            for y in range(columns):
                openFile.write(self.board[x][y]) 
            if x != rows-1:
                openFile.write("\n")
                
        openFile.close()
        return

# Counter function will count non water and non 0 pieces
def state_counter(currState):
    
    # First, reset all counts
    currState.rowPieceCounter = [0] * rows
    currState.columnPieceCounter = [0] * columns
    currState.totalPieceCount = 0
    currState.totalEmptySpots = 0
    currState.submarineCount = 0
    currState.destroyerCount = 0
    currState.cruiserCount = 0
    currState.battleshipCount = 0
    
    for x in range(rows):
        for y in range(columns):
            if currState.board[x][y] != '0' and currState.board[x][y] != 'W':
                currState.totalPieceCount += 1
                currState.rowPieceCounter[x] += 1
                currState.columnPieceCounter[y] += 1
                
                if currState.board[x][y] == 'S':
                    currState.submarineCount += 1
                    
                elif y + 1 < columns and currState.board[x][y] == 'L' and currState.board[x][y+1] == 'R':
                    currState.destroyerCount += 1
                
                elif x + 1 < rows and currState.board[x][y] == 'T' and currState.board[x+1][y] == 'B':
                    currState.destroyerCount += 1
                    
                elif y + 2 < columns and currState.board[x][y] == 'L' and currState.board[x][y+1] == 'M' and currState.board[x][y+2] == 'R':
                    currState.cruizerCount += 1
                
                elif x + 2 < rows and currState.board[x][y] == 'T' and currState.board[x+1][y] == 'M' and currState.board[x+2][y] == 'B':
                    currState.cruizerCount += 1
                
                elif y + 3 < columns and currState.board[x][y] == 'L' and currState.board[x][y+1] == 'M' and currState.board[x][y+2] == 'M' and currState.board[x][y+3] == 'R':
                    currState.battleshipCount += 1
                
                elif x + 3 < rows and currState.board[x][y] == 'T' and currState.board[x+1][y] == 'M' and currState.board[x+2][y] == 'M' and currState.board[x+3][y] == 'B':
                    currState.battleshipCount += 1
                    
    currState.totalEmptySpots = rows * columns - currState.totalPieceCount
                
# Process the current state of the board by row and column checking
def pre_process_by_row_and_col(currState):
    for x in range(rows):
        if rowConstraint[x] == currState.rowPieceCounter[x]:
            for y in range(columns):
                if currState.board[x][y] == '0':
                    currState.board[x][y] = 'W'
        
        elif rowConstraint[x] == 0:
            for y in range(columns):
                currState.board[x][y] = 'W'
                
    for y in range(columns):
        if columnConstraint[y] == currState.columnPieceCounter[y]:
            for x in range(rows):
                if currState.board[x][y] == '0':
                    currState.board[x][y] = 'W'
                
        elif columnConstraint[y] == 0:
            for x in range(rows):
                currState.board[x][y] = 'W'

# Process the current state of the board by piece checking
def pre_process_by_piece(currState):
    for x in range(rows):
        for y in range(columns):
            
            # If current square is a no hint square
            if currState.board[x][y] == '0' or currState.board[x][y] == 'W':
                continue
            
            # If current square is a submarine square
            elif currState.board[x][y] == 'S':
                for a in range(x-1, x+2):
                    for b in range(y-1, y+2):
                        if a >= 0 and a < rows and b >= 0 and b < columns:
                            if a == x and b == y:
                                continue
                            currState.board[a][b] = 'W'
            
            # If current square is a left piece square:
            elif currState.board[x][y] == 'L':
                for a in range(x-1, x+2):
                    for b in range(y-1, y+2):
                        if a >= 0 and a < rows and b >= 0 and b < columns:
                            if (a == x and b == y) or (a == x and b == y+1):
                                continue
                            currState.board[a][b] = 'W'
                            
            # If current square is a right piece square:
            elif currState.board[x][y] == 'R':
                for a in range(x-1, x+2):
                    for b in range(y-1, y+2):
                        if a >= 0 and a < rows and b >= 0 and b < columns:
                            if (a == x and b == y) or (a == x and b == y-1):
                                continue
                            currState.board[a][b] = 'W'
            
            # If current square is a top piece square:
            elif currState.board[x][y] == 'T':
                for a in range(x-1, x+2):
                    for b in range(y-1, y+2):
                        if a >= 0 and a < rows and b >= 0 and b < columns:
                            if (a == x and b == y) or (a == x+1 and b == y):
                                continue
                            currState.board[a][b] = 'W'
            
            # If current square is a bottom piece square:                            
            elif currState.board[x][y] == 'T':
                for a in range(x-1, x+2):
                    for b in range(y-1, y+2):
                        if a >= 0 and a < rows and b >= 0 and b < columns:
                            if (a == x and b == y) or (a == x-1 and b == y):
                                continue
                            currState.board[a][b] = 'W'
            
            # If current square is a middle piece square:                            
            elif currState.board[x][y] == 'T':
                for a in range(x-1, x+2):
                    for b in range(y-1, y+2):
                        if a >= 0 and a < rows and b >= 0 and b < columns:
                            if a == x or b == y:
                                continue
                            currState.board[a][b] = 'W'
                
# Could keep a count of all non water and non 0 pieces then compare that count after
# preprocessing and if its not the same then there's a problem        

# GAC Algorithm
def algorithm_GAC(currState):
         
    
# Main Function to process input, run GAC Algorithm, and provide output
if __name__ == "__main__":
    # inputConfigurationFile = sys.argv[1]
    # outputConfigurationFile = sys.argv[2]
    
    # Testing inputs and outputs
    inputConfigurationFile = "Intro to AI Projects\Battleship Solitaire Game AI\input_easy1.txt"
    outputConfigurationFile = "Intro to AI Projects\Battleship Solitaire Game AI\solution_easy11.txt"
    
    initialClass = State()
    initialClass.process_input(inputConfigurationFile)
    
    state_counter(initialClass)
    pre_process_by_row_and_col(initialClass)
    pre_process_by_piece(initialClass)
    
    # Running General-Arc-Consistency algorithm on the input
    #bestMove, value = algorithm_GAC(initialClass, 12, True, -inf, inf)
    initialClass.process_output(outputConfigurationFile)