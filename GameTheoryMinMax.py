from pip._vendor.distlib.compat import raw_input
USER_CHAR = 'X'
COMPUTER_CHAR = 'O'
MAX_ACTION_POSSIBLE = 8
MIN_ACTION_POSSIBLE = 0

#Class which maintains the state of Tic-Tac Toe Matrix 
class TicTacToeState(object):
    def __init__(self):
        self.TicTacMatrix = [['_' for rows in range(3)] for columns in range(3)]
        self.actionFromParent = 0
    
    # Set the Action to be done from the parent to get to this state.
    def setActionFromParent(self, move):
        self.actionFromParent = move
        
    # Get the Action to be done from the parent state
    def getActionFromParent(self):
        return self.actionFromParent
    
    # Copy the state value from the given Tic Tac Toe object
    def copyState(self, TicTacToe):
        for rows in range(3):
            for columns in range(3):
                    self.TicTacMatrix[rows][columns] = TicTacToe.TicTacMatrix[rows][columns]  
    # Make a move for the Given game Piece
    
    def makeMove(self, row, column, gamePiece):
        self.TicTacMatrix[row][column] = gamePiece;
    
    # Get user Move
    def getUserMove(self):
        userMove = (raw_input('Enter any positional index   '))
        userMove = int(userMove)
        if(userMove < MIN_ACTION_POSSIBLE) | (userMove > MAX_ACTION_POSSIBLE):
            print("This action is not possible!!")
        elif self.TicTacMatrix[int(userMove / 3)][userMove % 3] is not '_' :
            print("Invalid Move")
        else:
            self.TicTacMatrix[int(userMove / 3)][userMove % 3] = USER_CHAR

    # Display Tic-Tac Matrix
    def printTicTacBoard(self):
        for rows in range(3):
            for columns in range(3):
                print(self.TicTacMatrix[rows][columns], end='  ')
            print('\n')
    #
    #Check if the GamePiece won the game by checking the rows, columns and diagnols
    #
    def didLastMoveWin(self, gamePiece):
        #Check the rows for 3 game pieces
        for rows in range(3):
            count = 0;
            # Check if there are 3 gamePieces in a row or column
            for columns in range(3):
                if(self.TicTacMatrix[rows][columns] is not gamePiece):
                    break;
                else:
                    count = count + 1;
            if(count == 3):
                return True    
        #
        #Check the columns for 3 game pieces
        for cols in range(3):
            count = 0;
            for rows in range(3):
                if(self.TicTacMatrix[rows][cols] is not gamePiece):
                    break;
                else:
                    count = count + 1;
            if(count == 3):
                return True    
        
        # Check Diagnol for 3 game pieces
        frontDiagcount = 0;
        endDiagCount = 0;
        for index in range(3):
            if(self.TicTacMatrix[index][index] is  gamePiece):
                frontDiagcount = frontDiagcount + 1
            if(self.TicTacMatrix[2 - index][index] is  gamePiece):
                endDiagCount = endDiagCount + 1
        if(frontDiagcount == 3) | (endDiagCount == 3):
            return True;
        
        return False;   
    
    # Check if all the cells are full or we have a winner.
    def isGameOver(self):
        if (self.didLastMoveWin(USER_CHAR) | self.didLastMoveWin(COMPUTER_CHAR)):
            return True
        for rows in range(3):
            for columns in range(3):
                if(self.TicTacMatrix[rows][columns] is '_'):
                    return False;

        return True
    
    
    # utility function that gives the utility value of a given terminal state
    def utilityValueComputer(self):
        if(self.didLastMoveWin(USER_CHAR)):
            return -1;
        if(self.didLastMoveWin(COMPUTER_CHAR)):
            return 1;
        if(self.isGameOver()):
            return 0;
        
    # Regular Max Algorithm        
    def RegularMaxMove(self):
        possibleTicTacToe = [];
        neighborCount = 0;
        # compute all neighbors
        for rows in range(3) :  
            for columns in range(3):
                if(self.TicTacMatrix[rows][columns] is'_') :
                    # Create a neighbor state
                    neighborState = TicTacToeState(); 
                    neighborState.copyState(self)
                    neighborState.makeMove(rows, columns, COMPUTER_CHAR);
                    neighborState.setActionFromParent(rows * 3 + columns)
                    # Add it to the List and increase the neighbor count
                    possibleTicTacToe.append(neighborState)
                    neighborCount = neighborCount + 1
        # set the Maximum value and start looking for Max values
        currentMaxValue = -9999
        nodesVisited = neighborCount;
        for neigbor in range(neighborCount) :
            if possibleTicTacToe[neigbor].isGameOver(): 
                currentUtilityvalue = possibleTicTacToe[neigbor].utilityValueComputer();
            else:
                currentUtilityvalue, action, currentVisitedNodes = possibleTicTacToe[neigbor].RegularMinMove()
                nodesVisited = nodesVisited + currentVisitedNodes
            if(currentUtilityvalue > currentMaxValue):
                currentMaxValue = currentUtilityvalue
                maxNeighbor = possibleTicTacToe[neigbor]                   
        return currentMaxValue, maxNeighbor.getActionFromParent(), nodesVisited;

    # Regular Min Algorithm        
    def RegularMinMove(self):
        possibleTicTacToe = [];
        neighborCount = 0;
        # compute all neighbors
        for rows in range(3) :  
            for columns in range(3):
                if(self.TicTacMatrix[rows][columns] is'_') :
                    # Create a neighbor state
                    neighborState = TicTacToeState(); 
                    neighborState.copyState(self)
                    neighborState.makeMove(rows, columns, USER_CHAR);
                    neighborState.setActionFromParent(rows * 3 + columns)
                    # Add it to the List and increase the neighbor count
                    possibleTicTacToe.append(neighborState)
                    neighborCount = neighborCount + 1
        # set the Maximum value and start looking for Max values
        currentMinValue = 9999
        NodesVisited = neighborCount
        for neigbor in range(neighborCount) :
            if possibleTicTacToe[neigbor].isGameOver(): 
                utilityvalue = possibleTicTacToe[neigbor].utilityValueComputer();
            else:
                utilityvalue, action, currentNodesVisited = possibleTicTacToe[neigbor].RegularMaxMove()
                NodesVisited = NodesVisited + currentNodesVisited
            if(utilityvalue < currentMinValue):
                currentMinValue = utilityvalue
                minNeighbor = possibleTicTacToe[neigbor]
        return currentMinValue, minNeighbor.getActionFromParent(), NodesVisited;    
    
    # Alpha Beta Max Algorithm        
    def AlphaBetaMaxMove(self, alpha, beta):
        possibleTicTacToe = [];
        neighborCount = 0;
        # compute all neighbors
        for rows in range(3) :  
            for columns in range(3):
                if(self.TicTacMatrix[rows][columns] is'_') :
                    # Create a neighbor state
                    neighborState = TicTacToeState(); 
                    neighborState.copyState(self)
                    neighborState.makeMove(rows, columns, COMPUTER_CHAR);
                    neighborState.setActionFromParent(rows * 3 + columns)
                    # Add it to the List and increase the neighbor count
                    possibleTicTacToe.append(neighborState)
                    neighborCount = neighborCount + 1
        # set the Maximum value and start looking for Max values
        nodesVisited = neighborCount;
        currentMaxValue = -9999
        for neigbor in range(neighborCount) :
            # End Condition / Base Condition
            if possibleTicTacToe[neigbor].isGameOver(): 
                currentUtilityvalue = possibleTicTacToe[neigbor].utilityValueComputer();
            #
            # Check all the children for a Maximum utility value
            else:
                currentUtilityvalue, action, currentVisitedNodes = possibleTicTacToe[neigbor].AlphaBetaMinMove(alpha, beta)
                nodesVisited = nodesVisited + currentVisitedNodes   
                # Greater than Upper Limit, then return the value:
            if(currentUtilityvalue >= beta):
                return currentUtilityvalue, possibleTicTacToe[neigbor], nodesVisited
            # Update the Lower Limit (Alpha) 
            if(currentUtilityvalue >= alpha):
                alpha = currentUtilityvalue 
            
            if(currentUtilityvalue > currentMaxValue):
                currentMaxValue = currentUtilityvalue
                maxNeighbor = possibleTicTacToe[neigbor]
        return currentMaxValue, maxNeighbor.getActionFromParent(), nodesVisited;

    # Alpha Beta Min Algorithm        
    def AlphaBetaMinMove(self, alpha, beta):
        possibleTicTacToe = [];
        neighborCount = 0;
        # compute all neighbors
        for rows in range(3) :  
            for columns in range(3):
                if(self.TicTacMatrix[rows][columns] is'_') :
                    # Create a neighbor state
                    neighborState = TicTacToeState(); 
                    neighborState.copyState(self)
                    neighborState.makeMove(rows, columns, USER_CHAR);
                    neighborState.setActionFromParent(rows * 3 + columns)
                    # Add it to the List and increase the neighbor count
                    possibleTicTacToe.append(neighborState)
                    neighborCount = neighborCount + 1
        # set the Maximum value and start looking for Max values
        nodesVisited = neighborCount;
        currentMinValue = 9999
        for neigbor in range(neighborCount) :
            # End Condition / Base Condition
            if possibleTicTacToe[neigbor].isGameOver(): 
                currentUtilityvalue = possibleTicTacToe[neigbor].utilityValueComputer();
            # Check all the children for a Maximum utility value
            else:
                currentUtilityvalue, action, currentVisitedNodes = possibleTicTacToe[neigbor].AlphaBetaMaxMove(alpha, beta)
                nodesVisited = nodesVisited + currentVisitedNodes   
                # Lesser than Lower Limit, then return the value:
            if(currentUtilityvalue <= alpha):
                return currentUtilityvalue, possibleTicTacToe[neigbor], nodesVisited
            # Update the Upper Limit (Beta) 
            if(currentUtilityvalue <= beta):
                beta = currentUtilityvalue 
            
            if(currentUtilityvalue < currentMinValue):
                currentMinValue = currentUtilityvalue
                minNeighbor = possibleTicTacToe[neigbor]
        return currentMinValue, minNeighbor.getActionFromParent(), nodesVisited;

    
    #Calls the Alpha Beta Pruning Algorithm and 
    def runAlphaBetaPruningMinMax(self):
        maxValue, action, totalNodesVisited = self.AlphaBetaMaxMove(-9999, 9999);
        print("\t*****Visited Nodes**** ", totalNodesVisited)
        print("Running Alpha Beta Pruning. Computer's next move is ", action)
        if(action <= MAX_ACTION_POSSIBLE) | (action >= MIN_ACTION_POSSIBLE):
            self.TicTacMatrix[int(action / 3)][action % 3] = COMPUTER_CHAR
        else :
            print("")
    
    
    def runMinMax(self):
        maxValue, action, NodesVisted = self.RegularMaxMove();
        print("\t*****Visited Nodes**** ", NodesVisted)
        print("Running Regular Min-max. Computer's next move is", action)
        if(action <= MAX_ACTION_POSSIBLE) | (action >= MIN_ACTION_POSSIBLE):
            self.TicTacMatrix[int(action / 3)][action % 3] = COMPUTER_CHAR


    # Plays the Game : User VS Computer mode
    def playGame(self):
        print("Starting the Game")
        continueGame = True;
        while(continueGame):
            print("Your Turn");
            self.getUserMove()
            self.printTicTacBoard()
            if(self.didLastMoveWin(USER_CHAR)):
                print("\tUser won the Game")
                return
            elif(self.isGameOver()):
                print("\tGame Tie")
                return;
            else:
                print("**********************************************")
                print("Computer's Turn")
                # Run two logics for the same board
                TicTacBoard = TicTacToeState();
                TicTacBoard.copyState(self)
                self.runMinMax();
                self.printTicTacBoard();
                TicTacBoard.runAlphaBetaPruningMinMax()
                TicTacBoard.printTicTacBoard()
                if(self.didLastMoveWin(COMPUTER_CHAR) | TicTacBoard.didLastMoveWin(COMPUTER_CHAR)):
                    print("\tComputer Won the Game")
                    return;
                elif(self.isGameOver() | TicTacBoard.isGameOver()):
                    print("\tGame Tie!");
                    return;
def main():
    print("********************Tic-Tac-Toe-Player!!***************************")
    print("To play the game, enter the positional Index, your game piece will go the following position")
    print("\t0 1 2\n\t3 4 5\n\t6 7 8")
    TicTacToegame = TicTacToeState()
    # TicTacToegame.getUserMove()
    TicTacToegame.playGame()




main()
