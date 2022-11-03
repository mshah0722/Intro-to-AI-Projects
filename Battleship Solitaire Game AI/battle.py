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
        self.possibleSpots = {"Submarines": [], "Destroyers": [], "Cruisers": [], "Battleships": []}
        #self.evaluationValue = 0

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
                    currState.cruiserCount += 1
                
                elif x + 2 < rows and currState.board[x][y] == 'T' and currState.board[x+1][y] == 'M' and currState.board[x+2][y] == 'B':
                    currState.cruiserCount += 1
                
                elif y + 3 < columns and currState.board[x][y] == 'L' and currState.board[x][y+1] == 'M' and currState.board[x][y+2] == 'M' and currState.board[x][y+3] == 'R':
                    currState.battleshipCount += 1
                
                elif x + 3 < rows and currState.board[x][y] == 'T' and currState.board[x+1][y] == 'M' and currState.board[x+2][y] == 'M' and currState.board[x+3][y] == 'B':
                    currState.battleshipCount += 1
                    
            elif currState.board[x][y] == '0': 
                currState.totalEmptySpots += 1
                
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
            
            # If current square is a left piece square
            elif currState.board[x][y] == 'L':
                for a in range(x-1, x+2):
                    for b in range(y-1, y+2):
                        if a >= 0 and a < rows and b >= 0 and b < columns:
                            if (a == x and b == y) or (a == x and b == y+1):
                                continue
                            currState.board[a][b] = 'W'
                            
            # If current square is a right piece square
            elif currState.board[x][y] == 'R':
                for a in range(x-1, x+2):
                    for b in range(y-1, y+2):
                        if a >= 0 and a < rows and b >= 0 and b < columns:
                            if (a == x and b == y) or (a == x and b == y-1):
                                continue
                            currState.board[a][b] = 'W'
            
            # If current square is a top piece square
            elif currState.board[x][y] == 'T':
                for a in range(x-1, x+2):
                    for b in range(y-1, y+2):
                        if a >= 0 and a < rows and b >= 0 and b < columns:
                            if (a == x and b == y) or (a == x+1 and b == y):
                                continue
                            currState.board[a][b] = 'W'
            
            # If current square is a bottom piece square                           
            elif currState.board[x][y] == 'T':
                for a in range(x-1, x+2):
                    for b in range(y-1, y+2):
                        if a >= 0 and a < rows and b >= 0 and b < columns:
                            if (a == x and b == y) or (a == x-1 and b == y):
                                continue
                            currState.board[a][b] = 'W'
            
            # If current square is a middle piece square                           
            elif currState.board[x][y] == 'T':
                for a in range(x-1, x+2):
                    for b in range(y-1, y+2):
                        if a >= 0 and a < rows and b >= 0 and b < columns:
                            if a == x or b == y:
                                continue
                            currState.board[a][b] = 'W'
                
# Could keep a count of all non water and non 0 pieces then compare that count after
# preprocessing and if its not the same then there's a problem 

#https://discord.com/channels/892816026855690250/892816026855690254/1037403661741084672       

# Check if this piece is surrounded by water
def check_if_surrounded_by_water(currState, x, y):
    for a in range(x-1, x+2):
        for b in range(y-1, y+2):
            if a >= 0 and a < rows and b >= 0 and b < columns:
                if a == x and b == y:
                    continue
                if currState.board[a][b] != 'W':
                    return False
    return True

# Fill in the obvious submarine spots
def fill_in_submarine_spots(currState):
    for x in range(rows):
        for y in range(columns):
            
            # If current square is a no hint square
            if currState.board[x][y] == '0':
                if check_if_surrounded_by_water(currState, x, y):
                    if currState.rowPieceCounter[x] < rowConstraint[x] and currState.columnPieceCounter[y] < columnConstraint[y] and currState.submarineCount < ships['Submarines']:
                        currState.board[x][y] = 'S'
                        currState.rowPieceCounter[x] += 1 
                        currState.columnPieceCounter[y] += 1
                        currState.totalPieceCount += 1
                        currState.totalEmptySpots -= 1
                        currState.submarineCount += 1

# Check if any row or column constraints are violated
def check_if_row_column_constraints_violated(currState):
    # rowTotal = [sum(x) for x in currState.board]
    # colTotal = map(sum,zip(*currState.board))
    for x in range(rows):
        if currState.rowPieceCounter[x] > rowConstraint[x] or currState.columnPieceCounter[x] > columnConstraint[x]:
            return True
    
    return False

# Check if any piece constraints are violated
def check_if_piece_constraints_violated(currState):
    if (currState.submarineCount > ships['Submarines'] or currState.destroyerCount > ships['Destroyers'] or
        currState.cruiserCount > ships['Cruisers'] and currState.battleshipCount > ships['Battleships']):
        return True
    
    return False

# Check if all row and column constraints are satisfied
def check_if_row_column_constraints_met(currState):
    # rowTotal = [sum(x) for x in currState.board]
    # colTotal = map(sum,zip(*currState.board))

    if currState.rowPieceCounter == rowConstraint and currState.columnPieceCounter == columnConstraint:
        return True
    
    return False

# Check if piece constraints are satisfied
def check_if_piece_constraints_met(currState):
    if (currState.submarineCount == ships['Submarines'] and currState.destroyerCount == ships['Destroyers'] and
        currState.cruiserCount == ships['Cruisers'] and currState.battleshipCount == ships['Battleships']):
        return True
    
    return False

# Check if the grid is full
def check_if_grid_full(currState):
    if currState.totalEmptySpots != 0:
        return False    
    return True

# Get all possible moves
def get_all_possible_moves(currState):
    
    # Reset all possible moves
    currState.possibleSpots = {"Submarines": [], "Destroyers": [], "Cruisers": [], "Battleships": []}
    
    for x in range(rows):
        for y in range(columns):
            # There is a 'no hint spot' here
            if currState.board[x][y] == '0':
                if currState.submarineCount < ships['Submarines']:
                    # This is added to possible submarine locations
                    currState.possibleSpots['Submarines'].append([[x, y]])
                
                if y + 1 < columns and currState.board[x][y] == '0' and currState.board[x][y+1] == '0':
                    if currState.destroyerCount < ships['Destroyers']:
                        # This is added to possible destroyers locations with horizontal alignment
                        currState.possibleSpots['Destroyers'].append([[x, y], [x, y+1]])
                    
                    if y + 2 < columns and currState.board[x][y] == '0' and currState.board[x][y+1] == '0' and currState.board[x][y+2] == '0':
                        if currState.cruiserCount < ships['Cruisers']:
                            # This is added to possible cruisers locations with horizontal alignment
                            currState.possibleSpots['Cruisers'].append([[x, y], [x, y+1], [x, y+2]])
                        
                        if y + 3 < columns and currState.board[x][y] == '0' and currState.board[x][y+1] == '0' and currState.board[x][y+2] == '0' and currState.board[x][y+3] == '0':
                            if currState.battleshipCount < ships['Battleships']:
                                # This is added to possible battleship locations with horizontal alignment
                                currState.possibleSpots['Battleships'].append([[x, y], [x, y+1], [x, y+2], [x, y+3]])
                
                if x + 1 < rows and currState.board[x][y] == '0' and currState.board[x+1][y] == '0':
                    if currState.destroyerCount < ships['Destroyers']:
                        # This is added to possible destroyers locations with vertical alignment
                        currState.possibleSpots['Destroyers'].append([[x, y], [x+1, y]])
                
                    if x + 2 < rows and currState.board[x][y] == '0' and currState.board[x+1][y] == '0' and currState.board[x+2][y] == '0':
                        if currState.cruiserCount < ships['Cruisers']:
                            # This is added to possible cruisers locations with vertical alignment
                            currState.possibleSpots['Cruisers'].append([[x, y], [x+1, y], [x+2, y]])
                
                        if x + 3 < rows and currState.board[x][y] == '0' and currState.board[x+1][y] == '0' and currState.board[x+2][y] == '0' and currState.board[x+3][y] == '0':
                            if currState.battleshipCount < ships['Battleships']:
                                # This is added to possible battleship locations with vertical alignment
                                currState.possibleSpots['Battleships'].append([[x, y], [x+1, y], [x+2, y], [x+3, y]])

    return

# Return an unassigned variable with the smallest possible values
def return_MRV_variable(currState):
    minValue = inf
    minVariable = ''
    
    for ship in currState.possibleSpots:
        if len(currState.possibleSpots[ship]) == 0:
            continue
            
        if minValue > len(currState.possibleSpots[ship]):
            minValue = len(currState.possibleSpots[ship])
            minVariable = ship
    
    return minVariable            

# Check if piece is horizontal or vertical
def check_if_horizontal_or_vertical(position):
    # If alignment is horizontal
    if position[0][0] == position[1][0]:
        return True
    # If alignment is vertical
    else:
        return False
    
# Insert the ship into the board at given position
def insert_ship_at_position(currState, ship, position):
    if ship == 'Submarines' and len(position) == 1:
        currState.board[position[0][0]][position[0][1]] = 'S'
        currState.rowPieceCounter[position[0][0]] += 1
        currState.columnPieceCounter[position[0][1]] += 1
        currState.totalPieceCount += 1
        currState.totalEmptySpots -= 1
        currState.submarineCount += 1
    elif ship == 'Destroyers' and len(position) == 2 and check_if_horizontal_or_vertical(position):
        currState.board[position[0][0]][position[0][1]] = 'L'
        currState.board[position[1][0]][position[1][1]] = 'R'
        currState.rowPieceCounter[position[0][0]] += 1
        currState.columnPieceCounter[position[0][1]] += 1
        currState.rowPieceCounter[position[1][0]] += 1
        currState.columnPieceCounter[position[1][1]] += 1
        currState.totalPieceCount += 2
        currState.totalEmptySpots -= 2
        currState.destroyerCount += 1
    elif ship == 'Destroyers' and len(position) == 2 and not check_if_horizontal_or_vertical(position):
        currState.board[position[0][0]][position[0][1]] = 'T'
        currState.board[position[1][0]][position[1][1]] = 'B'
        currState.rowPieceCounter[position[0][0]] += 1
        currState.columnPieceCounter[position[0][1]] += 1
        currState.rowPieceCounter[position[1][0]] += 1
        currState.columnPieceCounter[position[1][1]] += 1
        currState.totalPieceCount += 2
        currState.totalEmptySpots -= 2
        currState.destroyerCount += 1
    elif ship == 'Cruisers' and len(position) == 3 and check_if_horizontal_or_vertical(position):
        currState.board[position[0][0]][position[0][1]] = 'L'
        currState.board[position[1][0]][position[1][1]] = 'M'
        currState.board[position[2][0]][position[2][1]] = 'R'
        currState.rowPieceCounter[position[0][0]] += 1
        currState.columnPieceCounter[position[0][1]] += 1
        currState.rowPieceCounter[position[1][0]] += 1
        currState.columnPieceCounter[position[1][1]] += 1
        currState.rowPieceCounter[position[2][0]] += 1
        currState.columnPieceCounter[position[2][1]] += 1
        currState.totalPieceCount += 3
        currState.totalEmptySpots -= 3
        currState.cruiserCount += 1
    elif ship == 'Cruisers' and len(position) == 3 and not check_if_horizontal_or_vertical(position):
        currState.board[position[0][0]][position[0][1]] = 'T'
        currState.board[position[1][0]][position[1][1]] = 'M'
        currState.board[position[2][0]][position[2][1]] = 'B'
        currState.rowPieceCounter[position[0][0]] += 1
        currState.columnPieceCounter[position[0][1]] += 1
        currState.rowPieceCounter[position[1][0]] += 1
        currState.columnPieceCounter[position[1][1]] += 1
        currState.rowPieceCounter[position[2][0]] += 1
        currState.columnPieceCounter[position[2][1]] += 1
        currState.totalPieceCount += 3
        currState.totalEmptySpots -= 3
        currState.cruiserCount += 1
    elif ship == 'Battleships' and len(position) == 4 and check_if_horizontal_or_vertical(position):
        currState.board[position[0][0]][position[0][1]] = 'L'
        currState.board[position[1][0]][position[1][1]] = 'M'
        currState.board[position[2][0]][position[2][1]] = 'M'
        currState.board[position[3][0]][position[3][1]] = 'R'
        currState.rowPieceCounter[position[0][0]] += 1
        currState.columnPieceCounter[position[0][1]] += 1
        currState.rowPieceCounter[position[1][0]] += 1
        currState.columnPieceCounter[position[1][1]] += 1
        currState.rowPieceCounter[position[2][0]] += 1
        currState.columnPieceCounter[position[2][1]] += 1
        currState.rowPieceCounter[position[3][0]] += 1
        currState.columnPieceCounter[position[3][1]] += 1
        currState.totalPieceCount += 4
        currState.totalEmptySpots -= 4
        currState.battleshipCount += 1
    elif ship == 'Battleships' and len(position) == 4 and not check_if_horizontal_or_vertical(position):
        currState.board[position[0][0]][position[0][1]] = 'T'
        currState.board[position[1][0]][position[1][1]] = 'M'
        currState.board[position[2][0]][position[2][1]] = 'M'
        currState.board[position[3][0]][position[3][1]] = 'B'
        currState.rowPieceCounter[position[0][0]] += 1
        currState.columnPieceCounter[position[0][1]] += 1
        currState.rowPieceCounter[position[1][0]] += 1
        currState.columnPieceCounter[position[1][1]] += 1
        currState.rowPieceCounter[position[2][0]] += 1
        currState.columnPieceCounter[position[2][1]] += 1
        currState.rowPieceCounter[position[3][0]] += 1
        currState.columnPieceCounter[position[3][1]] += 1
        currState.totalPieceCount += 4
        currState.totalEmptySpots -= 4
        currState.battleshipCount += 1

# Enforce General Arc Consistency and prune all inconsistent arcs    
def enforce_GAC(currState):
    
    # Ensure that there are spots available for the ships that still need to be placed, otherwise prune branch
    if currState.submarineCount != ships['Submarines'] and len(currState.possibleSpots["Submarines"]) == 0:
        return "DWO"
    elif currState.destroyerCount != ships['Destroyers'] and len(currState.possibleSpots["Destroyers"]) == 0:
        return "DWO"
    elif currState.cruiserCount != ships['Cruisers'] and len(currState.possibleSpots["Cruisers"]) == 0:
        return "DWO"
    elif currState.battleshipCount != ships['Battleships'] and len(currState.possibleSpots["Battleships"]) == 0:
        return "DWO"
    
    return algorithm_GAC(currState)
    
    
    
# GAC Algorithm
def algorithm_GAC(currState):    
    # If all variables are assigned:
    if check_if_row_column_constraints_met(currState) and check_if_piece_constraints_met(currState) and check_if_grid_full(currState):
        return currState
    
    # Pick an unassigned variable
    chosenShip = return_MRV_variable(currState)
    
    # Go through all possible spots for the ship
    for spot in currState.possibleSpots[chosenShip]:
        # In the new State, insert the ship at the spot
        newState = copy.deepcopy(currState)
        insert_ship_at_position(newState, chosenShip, spot)
        
        # Prune all values of grid with preprocessing steps
        state_counter(newState)
        pre_process_by_row_and_col(newState)
        pre_process_by_piece(newState)
        state_counter(newState)
        fill_in_submarine_spots(newState)
        pre_process_by_row_and_col(newState)
        state_counter(newState)
        
        # Go through all the constraints and make sure they aren't violated
        if check_if_row_column_constraints_violated(newState) or check_if_piece_constraints_violated(newState):
            # If violated, then try next position
            continue
        
        else:
            get_all_possible_moves(newState)
            result = enforce_GAC(newState)
            # child returns DWO
            if result == "DWO":
                continue
            else:
                return result
         
    return result


# def GAC_Enforce:
    
    
           
# FC Algorithm
# def algorithm_FC(currState):
#     # If all variables are assigned:
#     if check_if_grid_full(currState):
#         return currState
    
#     # Pick an unassigned variable
#     chosenShip = MRV(currState)
#     assigned[chosenShip] = True
    
#     preprocess(currState)
    
#     for val in currState.possibleSpots[var]:
#         DWO = False

#         stored_possibleSpots = deepcopy(currState.possibleSpots)
#         newState = deepcopy(currState.currState.board)
#         insert_into_board(newState, var, val)  # new board with the ship placed
#         new_possibleSpots = deepcopy(currState.possibleSpots)
#         new_possibleSpots[var].remove(val)
#         child = State(parent=currState, currState.board=newState,
#                       possibleSpots=new_possibleSpots, dim=currState.dim)

#         # all constraints related to this var
#         consts = find_constraints(newState, var, val)

#         while consts:
#             const = consts.pop()
#             # C has only one unassigned variable X in its scope
#             if FCCheck(child, const, possibleSpots) == 'DWO':
#                 DWO = True
#                 break
#         if not DWO:  # all constraints consistent
#             FC(currState, level+1)
#         currState.possibleSpots = stored_possibleSpots
#     assigned[var_y][var_x] = False  # undo since we have tried all of V's value
#     return
    

# BT Algorithm
def algorithm_BT(currState):
    # If all variables are assigned:
    if check_if_grid_full(currState):
        return currState
    
        
    
# Main Function to process input, run GAC Algorithm, and provide output
if __name__ == "__main__":
    # inputConfigurationFile = sys.argv[1]
    # outputConfigurationFile = sys.argv[2]
    
    # Testing inputs and outputs
    inputConfigurationFile = "Intro to AI Projects\Battleship Solitaire Game AI\input_easy1.txt"
    outputConfigurationFile = "Intro to AI Projects\Battleship Solitaire Game AI\solution_easy11.txt"
    
    initialState = State()
    initialState.process_input(inputConfigurationFile)
    
    state_counter(initialState)
    pre_process_by_row_and_col(initialState)
    pre_process_by_piece(initialState)
    state_counter(initialState)
    fill_in_submarine_spots(initialState)
    pre_process_by_row_and_col(initialState)
    state_counter(initialState)
    # val = check_if_row_column_constraints_met(initialState)
    get_all_possible_moves(initialState)
    # return_MRV_variable(initialState)
    finalState = algorithm_GAC(initialState)
    
    # Running General-Arc-Consistency algorithm on the input
    #bestMove, value = algorithm_GAC(initialState, 12, True, -inf, inf)
    finalState.process_output(outputConfigurationFile)