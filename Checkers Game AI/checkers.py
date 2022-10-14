# Global imports
from audioop import reverse
import sys
import copy
from math import inf

# Global variables for max rows and columns
rows = 8
columns = 8

# Main class to store the state 
class State:
    
    # Initialize the object's attributes 
    def __init__(self):
        # If currPlayer is True, then player is Red, otherwise Black
        self.currPlayer = True
        self.board = []
        self.blackPieceCount = 0
        self.redPieceCount = 0
        self.evaluationValue = 0
        self.gameOver = False
        self.changeX = [1,1,-1,-1]
        self.changeY = [1,-1,1,-1]  
    
    # Check if the new checkers board is the same as the existing one
    def __eq__(self, other):
        for x in range(rows):
            for y in range(columns):
                if self.board[x][y] != other.board[x][y]:
                    return False

        return True
        
    # Process the initial board configuration file
    def process_input(self, file):
        openFile = open(file, 'r')
        allLines = openFile.readlines()
        cols = []
        
        # Iterate through the lines and store the board configuration in self.board
        for line in allLines:
            for i in range(columns):
                position = line[i]
                if position == 'r' or position == 'R':
                    self.redPieceCount +=1
                elif position == 'b' or position == 'B':
                    self.blackPieceCount +=1
                cols.append(position)
                
            self.board.append(cols)
            cols = []
        evaluation = evaluate_state(self)
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
    
# Check if the move is a legal diagonal move for normal red or black piece
def check_if_legal_diagonal_move_normal_piece(currState, x1, y1, x2, y2):
    if (currState.currPlayer == True) and (x2 == x1 + 1 or x2 == x1 - 1) and (y2 == y1 - 1):
        return True
    if (currState.currPlayer == False) and (x2 == x1 + 1 or x2 == x1 - 1) and (y2 == y1 + 1):
        return True
    return False

# Check if the move is a legal diagonal move for red king or black king
def check_if_legal_diagonal_move_king_piece(currState, x1, y1, x2, y2):
    if (currState.currPlayer == True) and (x2 == x1 + 1 or x2 == x1 - 1) and (y2 == y1 + 1 or y2 == y1 - 1):
        return True
    if (currState.currPlayer == False) and (x2 == x1 + 1 or x2 == x1 - 1) and (y2 == y1 + 1 or y2 == y1 - 1):
        return True
    return False

# Check if the move is a legal diagonal jump for normal red or black piece
def check_if_legal_diagonal_jump_normal_piece(currState, x1, y1, x2, y2):
    if (currState.currPlayer == True) and (x2 == x1 + 2 or x2 == x1 - 2) and (y2 == y1 - 2):
        return True
    if (currState.currPlayer == False) and (x2 == x1 + 2 or x2 == x1 - 2) and (y2 == y1 + 2):
        return True
    return False

# Check if the move is a legal diagonal jump for red king or black king
def check_if_legal_diagonal_jump_king_piece(currState, x1, y1, x2, y2):
    if (currState.currPlayer == True) and (x2 == x1 + 2 or x2 == x1 - 2) and (y2 == y1 + 2 or y2 == y1 - 2):
        return True
    if (currState.currPlayer == False) and (x2 == x1 + 2 or x2 == x1 - 2) and (y2 == y1 + 2 or y2 == y1 - 2):
        return True
    return False

# Check if the pieve being jumped is enemy peice
def check_if_jump_piece_is_enemy(currState, x1, y1, x2, y2):
    assert (abs(x1 - x2) == abs(y1 - y2) == 2)
    
    x3 = (x1+x2) //2
    y3 = (y1+y2) //2
    
    if (currState.currPlayer == True and (currState.board[x3][y3] == 'b' or currState.board[x3][y3] == 'B')):
        return True
    if (currState.currPlayer == False and (currState.board[x3][y3] == 'r' or currState.board[x3][y3] == 'R')):
        return True
    return False

# Check if the move is legal diagonal move
def check_if_legal_diagonal_move(currState, x1, y1, x2, y2):
    # Make sure x1, y1, x2, y2 ar all within the ranges of the board
    if not (0 <= x1 <= rows - 1
        and 0 <= y1 <= columns - 1
        and 0 <= x2 <= rows - 1
        and 0 <= y2 <= columns - 1):
        return False
    
    piece = currState.board[x1][y1]
    
    # Confirming that the current piece is for our colour
    if currState.currPlayer == True:
        if piece == 'b' or piece == 'B':
            return False
    elif currState.currPlayer == False:
        if piece == 'r' or  piece == 'R':
            return False
    
    destinationSpot = currState.board[x2][y2]
      
    # Checks if the destination space is empty
    if destinationSpot != '.':
        return False
    
    # Checks if the move is a legal diagonal step or jump
    if not (check_if_legal_diagonal_move_normal_piece(currState, x1, y1, x2, y2) or check_if_legal_diagonal_move_king_piece(currState, x1, y1, x2, y2)):
        return False
    
    # Returns True if no rules are violated
    else:
        return True

# Check if the move is legal diagonal jump
def check_if_legal_diagonal_jump(currState, x1, y1, x2, y2):
    # Make sure x1, y1, x2, y2 ar all within the ranges of the board
    if not (0 <= x1 <= rows - 1
        and 0 <= y1 <= columns - 1
        and 0 <= x2 <= rows - 1
        and 0 <= y2 <= columns - 1):
        return False
    
    piece = currState.board[x1][y1]
    
    # Confirming that the current piece is for our colour
    if currState.currPlayer == True:
        if piece == 'b' or piece == 'B':
            return False
    elif currState.currPlayer == False:
        if piece == 'r' or  piece == 'R':
            return False
    
    destinationSpot = currState.board[x2][y2]
      
    # Checks if the destination space is empty
    if destinationSpot != '.':
        return False
    
    # Checks if the move is a legal diagonal step or jump
    if not (check_if_legal_diagonal_jump_normal_piece(currState, x1, y1, x2, y2) or check_if_legal_diagonal_jump_king_piece(currState, x1, y1, x2, y2)):
        return False
    
    # Checks if jumps are made over enemy pieces
    if ((check_if_legal_diagonal_jump_normal_piece(currState, x1, y1, x2, y2) or check_if_legal_diagonal_jump_king_piece(currState, x1, y1, x2, y2)) and not check_if_jump_piece_is_enemy(currState, x1, y1, x2, y2)):
        return False
    
    # Returns True if no rules are violated
    else:
        return True

# Capture opposition piece
def capture_opposition_piece(currState, x1, y1, x2, y2):
    assert (abs(x1 - x2) == abs(y1 - y2) == 2)
    
    x3 = (x1+x2) //2
    y3 = (y1+y2) //2
    
    if (currState.currPlayer == True):
        currState.board[x3][y3] = '.'
        currState.blackPieceCount -= 1      
    elif (currState.currPlayer == False):
        currState.board[x3][y3] = '.'
        currState.redPieceCount -=1
    return 
    
# Check if the game is over in the current State    
def check_if_game_over(currState):
    # Black won
    if currState.redPieceCount == 0:
        currState.gameOver = True
        return [True, 1] 
    # Red won
    elif currState.blackPieceCount == 0:
        currState.gameOver = True
        return [True, 0]
    # Both pieces still available
    else:
        return [False, -1]

# Check if we can now convert the piece to King    
def check_if_piece_is_now_king(currState, x1, y1):
    if ((currState.currPlayer == True) and (x1 == 0) and (currState.board[x1][y1] == 'r')):
        currState.board[x1][y1] = 'R'
        return True
    elif ((currState.currPlayer == False) and (x1 == rows - 1) and (currState.board[x1][y1] == 'b')):
        currState.board[x1][y1] = 'B'
        return True
    return False

# Check if we can do an additional jump
def check_for_extra_jump(currState, x, y):
    if currState.currPlayer:
        red = True
        possiblePlayerRed = ['r', 'R']
    else:
        red = False
        possiblePlayerBlack = ['b', 'B']
    
    # Check for all Red Pieces for moving up the board
    if (red and (currState.board[x][y] == possiblePlayerRed[0] or currState.board[x][y] == possiblePlayerRed[1])):
        if (x - 2 >= 0 and y + 2 < columns
            and currState.board[x-2][y+2] == '.'
            and check_if_jump_piece_is_enemy(currState, x, y, x-2, y+2)):
            
            return (x-2, y+2)
            #confirm_extra_jump(currState, x, y, x-2, y+2)
            
        if (x - 2 >= 0 and y - 2 >= 0
            and currState.board[x-2][y-2] == '.'
            and check_if_jump_piece_is_enemy(currState, x, y, x-2, y-2)):
            
            return (x-2, y-2)
            #confirm_extra_jump(currState, x, y, x-2, y-2)
        
        # Check for all Red Kings for moving down the board
        if currState.board[x][y] == possiblePlayerRed[1]:
            if (x + 2 < rows and y + 2 < columns
                and currState.board[x+2][y+2] == '.'
                and check_if_jump_piece_is_enemy(currState, x, y, x+2, y+2)):

                return (x+2, y+2)
                #confirm_extra_jump(currState, x, y, x+2, y+2)
            
            if (x + 2 < rows and y - 2 >= 0
                and currState.board[x+2][y-2] == '.'
                and check_if_jump_piece_is_enemy(currState, x, y, x+2, y-2)):

                return (x+2, y-2)
                #confirm_extra_jump(currState, x, y, x+2, y-2)

    # Check for all Black Pieces for moving down the board
    else:
        if (x + 2 < rows and y + 2 < columns
            and currState.board[x+2][y+2] == '.'
            and check_if_jump_piece_is_enemy(currState, x, y,  x+2, y+2)):
            
            return (x+2, y+2)
            #confirm_extra_jump(currState, x, y, x+2, y+2)
        
        if (x + 2 < rows and y - 2 >= 0
            and currState.board[x+2][y-2] == '.'
            and check_if_jump_piece_is_enemy(currState, x, y, x+2, y-2)):
            
            return (x+2, y-2)
            #confirm_extra_jump(currState, x, y, x+2, y-2)
            
        # Check for all Black Kings for moving up the board
        if currState.board[x][y] == possiblePlayerBlack[1]:
            if (x - 2 >= 0 and y + 2 < columns
                and currState.board[x-2][y+2] == '.'
                and check_if_jump_piece_is_enemy(currState, x, y, x-2, y+2)):
                
                return (x-2, y+2)
                #confirm_extra_jump(currState, x, y, x-2, y+2)
            
            if (x - 2 >= 0 and y - 2 >= 0
                and currState.board[x-2][y-2] == '.'
                and check_if_jump_piece_is_enemy(currState, x, y, x-2, y-2)):
                
                return (x-2, y-2)
                #confirm_extra_jump(currState, x, y, x-2, y-2)
    return (-1,-1)

# Evaluate the value of a state and return value
def evaluate_state(currState):
    redTotalValue = 0
    blackTotalValue = 0
    normalRedPieceCount = 0
    normalBlackPieceCount = 0
    kingRedPieceCount = 0
    kingBlackPieceCount = 0
    
    for x in range(rows):
        for y in range(columns):
            # Utility value for red pieces
            if currState.board[x][y] == 'r':
                normalRedPieceCount += 1
                # If red piece is higher up the board and centralized then better value since it could pottentially king
                if x < 4 and 1 < y < 6:
                    redTotalValue += 8
                # If red piece is higher up the board then better value since it could pottentially king
                elif x < 6:
                    redTotalValue += 6
                # Lower value for red piece lower in the board
                else:
                    redTotalValue += 5
            # Max value for Red King piece
            elif currState.board[x][y] == 'R':
                kingRedPieceCount += 1
                redTotalValue += 10
            
            # Utility value for black pieces    
            elif currState.board[x][y] == 'b':
                normalBlackPieceCount += 1
                # If black piece is lower down the board and centralized then better value since it could pottentially king
                if x > 4 and 1 < y < 6:
                    blackTotalValue += 8
                # If black piece is lower down the board then better value since it could pottentially king
                elif x > 2:
                    blackTotalValue += 6
                # Lower value for black piece higher in the board
                else:
                    blackTotalValue += 5
            # Max value for Black King piece
            elif currState.board[x][y] == 'B':
                kingBlackPieceCount += 1
                blackTotalValue += 10
    
    # If no red pieces on the board then black wins and value = -inf            
    if normalRedPieceCount + kingRedPieceCount == 0:
        currState.evaluationValue = -inf
        currState.gameOver = True
    
    # If no black pieces on the board then red wins and value = inf 
    elif normalBlackPieceCount + kingBlackPieceCount == 0:
        currState.evaluationValue = inf
        currState.gameOver = True
    
    # Utility value = redValue - blackValue
    else:
        currState.evaluationValue = redTotalValue - blackTotalValue
    return currState.evaluationValue

# Return a list of all possible moves for this player at position x1, y1
def get_possible_moves(currState, x1, y1):
    captureMoves = []
    normalMoves = []
    
    # If player is red, move up
    if currState.currPlayer == True:
        sign = -1
    else:
        sign = 1
    
    # Only move forward for normal pieces and move forward and backward for king pieces
    if currState.board[x1][y1] == 'B' or currState.board[x1][y1] == 'R':
        maxRange = 4
    else:
        maxRange = 2
        
    for i in range(maxRange):
        x2 = x1 + sign * currState.changeX[i]
        y2 = y1 + sign * currState.changeY[i]
        if check_if_legal_diagonal_move(currState, x1, y1, x2, y2):
            normalMoves.append((x2, y2))
        else:
            x2 += sign * currState.changeX[i]
            y2 += sign * currState.changeY[i]
            if check_if_legal_diagonal_jump(currState, x1, y1, x2, y2):
                captureMoves.append((x2, y2))

    return normalMoves, captureMoves

# Return a list of all possible states
def get_all_possible_moves(currState):
    captureMoves = []
    normalMoves = []
    
    if currState.currPlayer:
        possiblePlayer = ['r', 'R']
    else:
        possiblePlayer = ['b', 'B']
    
    # Go through all possible points in board and get their moves
    for x in range(rows):
        for y in range(columns):
            if (currState.board[x][y] != '.' and (currState.board[x][y] == possiblePlayer[0] or currState.board[x][y] == possiblePlayer[1])):
                normal, capture = get_possible_moves(currState, x, y)
                if len(normal) != 0:
                    normalMoves.append(((x, y), normal))
                if len(capture) != 0:
                    captureMoves.append(((x, y), capture))
                    
    # If we can capture any pieces then return capture moves
    if len(captureMoves) != 0:
        return captureMoves
    
    # Return normal moves
    return normalMoves

# Make a move
def make_a_move(currState, x1, y1, x2, y2):
    currState.board[x2][y2] = currState.board[x1][y1]
    currState.board[x1][y1] = '.'
    x3, y3 = -1, -1
    
    # Convert to king piece if possible
    flag = check_if_piece_is_now_king(currState, x2, y2)
    
    # Check if piece was captured by move
    if abs(x2 - x1) == 2:
        capture_opposition_piece(currState, x1, y1, x2, y2)
        if not flag:
            # Check for extra jumps, and do those jumps until no longer possible
            x3, y3 = check_for_extra_jump(currState, x2, y2)
            while(x3, y3) != (-1,-1):
                x3, y3 = make_a_move(currState, x2, y2, x3, y3)
        else:
            x3, y3 = -1, -1

    return x3, y3

# Mini-Max Algorithm
def mini_max_algorithm(currState, depth, currPlayer):
    if depth == 0 or check_if_game_over(currState)[0]:
        return None, evaluate_state(currState)
    bestMove = copy.deepcopy(currState)
    if currPlayer:
        maxEvaluation = -inf
        moves = get_all_possible_moves(currState)
        moves.sort(key=lambda move: len(move[1]))
        for move in moves:
            x1 = move[0][0]
            y1 = move[0][1]
            positions = move[1]
            for position in positions:
                x2 = position[0]
                y2 = position[1]
                nextState = copy.deepcopy(currState)
                a3, b3 = make_a_move(nextState, x1, y1, x2, y2)
                nextState.currPlayer = False
                state, eval = mini_max_algorithm(nextState, depth - 1, False)
                if eval > maxEvaluation:
                    maxEvaluation = eval
                    bestMove = copy.deepcopy(nextState)
        currState.evaluationValue = maxEvaluation
        return bestMove, maxEvaluation
    else:
        minEvaluation = inf
        moves = get_all_possible_moves(currState)
        for move in moves:
            x1 = move[0][0]
            y1 = move[0][1]
            positions = move[1]
            for position in positions:
                x2 = position[0]
                y2 = position[1]
                nextState = copy.deepcopy(currState)
                a3, b3 = make_a_move(nextState, x1, y1, x2, y2)
                nextState.currPlayer = True
                state, eval = mini_max_algorithm(nextState, depth - 1, True)
                if eval < minEvaluation:
                    minEvaluation = eval
                    bestMove = copy.deepcopy(nextState)
        currState.evaluationValue = minEvaluation
        return bestMove, minEvaluation

# Mini-max algorithm with alpha beta pruning
def alpha_beta(currState, depth, currPlayer, alpha, beta):
    if depth == 0 or check_if_game_over(currState)[0]:
        return None, evaluate_state(currState)
    bestMove = copy.deepcopy(currState)
    if currPlayer:
        maxEvaluation = -inf
        moves = get_all_possible_moves(currState)
        #moves.sort(key=lambda x: (abs(x[0][0] - x[1][0][0]) + abs(x[0][1] - x[1][0][1])), reverse=True)
        for move in moves:
            x1 = move[0][0]
            y1 = move[0][1]
            positions = move[1]
            for position in positions:
                x2 = position[0]
                y2 = position[1]
                nextState = copy.deepcopy(currState)
                a3, b3 = make_a_move(nextState, x1, y1, x2, y2)
                nextState.currPlayer = False
                state, eval = alpha_beta(nextState, depth - 1, False, alpha, beta)
                if eval > maxEvaluation:
                    maxEvaluation = eval
                    bestMove = copy.deepcopy(nextState)
                if maxEvaluation >= beta:
                    currState.evaluationValue = maxEvaluation
                    return bestMove, maxEvaluation
                alpha = max(alpha, maxEvaluation)
        currState.evaluationValue = maxEvaluation
        return bestMove, maxEvaluation
    else:
        minEvaluation = inf
        moves = get_all_possible_moves(currState)
        #moves.sort(key=lambda x: (abs(x[0][0] - x[1][0][0]) + abs(x[0][1] - x[1][0][1])), reverse=True)
        for move in moves:
            x1 = move[0][0]
            y1 = move[0][1]
            positions = move[1]
            for position in positions:
                x2 = position[0]
                y2 = position[1]
                nextState = copy.deepcopy(currState)
                a3, b3 = make_a_move(nextState, x1, y1, x2, y2)
                nextState.currPlayer = True
                state, eval = alpha_beta(nextState, depth - 1, True, alpha, beta)
                if eval < minEvaluation:
                    minEvaluation = eval
                    bestMove = copy.deepcopy(nextState)
                if minEvaluation <= alpha:
                    currState.evaluationValue = minEvaluation
                    return bestMove, minEvaluation
                beta = min(beta, minEvaluation)
        currState.evaluationValue = minEvaluation
        return bestMove, minEvaluation
          
if __name__ == "__main__":
    inputConfigurationFile = sys.argv[1]
    outputConfigurationFile = sys.argv[2]
    
    # Testing inputs and outputs
    # inputConfigurationFile = "checkers_validate\input3.txt"
    # outputConfigurationFile = "checkers_validate\solution33.txt"
    
    initialClass = State()
    initialClass.process_input(inputConfigurationFile)

    # Running mini-max algorithm only
    #bestMove, value = mini_max_algorithm(initialClass, 8, True)
    #bestMove.process_output(outputConfigurationFile)
    
    # Running mini-max algorithm with alpha beta pruning
    bestMove, value = alpha_beta(initialClass, 12, True, -inf, inf)
    bestMove.process_output(outputConfigurationFile)
    