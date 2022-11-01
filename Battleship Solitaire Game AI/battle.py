# Global imports
from audioop import reverse
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


if __name__ == "__main__":
    # inputConfigurationFile = sys.argv[1]
    # outputConfigurationFile = sys.argv[2]
    
    # Testing inputs and outputs
    inputConfigurationFile = "Battleship Solitaire Game AI/input_easy1.txt"
    outputConfigurationFile = "Battleship Solitaire Game AI/solution_easy11.txt"
    
    initialClass = State()
    initialClass.process_input(inputConfigurationFile)
    
    # Running General-Arc-Consistency algorithm on the input
    #bestMove, value = algorithm_GAC(initialClass, 12, True, -inf, inf)
    initialClass.process_output(outputConfigurationFile)