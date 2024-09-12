from enum import Enum

class Result(Enum):
    """ An Enumerator referenced by the Connect4 class to differentiate between different 'states' of the game.
    """
    NONE = 0
    P1WIN = 1
    P2WIN = 2
    DRAW = 3

class Connect4:
    """ A playable game of Connect4 with functions allowing it to be played with validation checks to find valid inputs and outcomes to the game. It updates properties of the object to reflect the current state of the game.
    """
    P1 = 1
    P2 = 2
    COLS = 0
    ROWS = 0

    def __init__(self, COLS, ROWS):
        """ Initialises the game object, creating a grid, a total occupied spaces per column, the current turn and the result of the game.

        Args:
            COLS (int): The number of columns desired in the grid
            ROWS (int): The number of rows desired in the grid
        """
        Connect4.COLS = COLS
        Connect4.ROWS = ROWS
        self.grid = self.create_grid()
        self.tot = self.create_tot()
        self.turn = Connect4.P1
        self.result = Result.NONE

    def create_grid(self):
        """ Returns a 2D array with ROWS number of rows and COLS number of columns, filled with zeroes, which represent empty spaces in the grid.

        Returns:
            2D array: An array containing ROWS arrays, each filled with COLS zeroes.
        """
        grid = []
        for i in range(Connect4.ROWS):  #Creating the blank 'rows'.
            grid.append([])
            for j in range(Connect4.COLS):  #Adding zeroes to each 'row'.
                grid[i].append(0)
        return grid

    def return_grid(self):
        """ Returns the grid.

        Returns:
            2D array: Represents the grid
        """
        return self.grid
    
    def create_tot(self):
        """ Returns an array of zeroes, COLS items long, representing the number of counters in each column of the grid.
        
        Returns:
            array: An array containing COLS zeroes
        """
        tot = []
        for i in range(Connect4.COLS):
            tot.append(0)
        return tot

    def valid_move(self, move):
        """ Returns False if the column specified by move is full or outside of the grid.

        Args:
            move (int): The column in which a move is trying to be made

        Returns:
            bool: Whether or not the move is valid
        """
        if self.tot[move] == Connect4.ROWS or move > Connect4.COLS-1 or move < 0:
            return False
        return True
    
    def change_turn(self):
        """ Changes the current turn
        """
        self.turn = Connect4.P2 if self.turn == Connect4.P1 else Connect4.P1

    def checkwin(self):
        """ Checks whether an outcome has been achieved. Checks if either all columns are full or if four adjacent spaces within the grid are not empty and are the same colour horizotally, vertically, or diagonally. 

        Returns:
            boolean: Whether or not an outcome has been reached
        """
        
        for row in self.grid:  #Remember grid upside down!
            for col in range(Connect4.COLS-3):  #Horizontal victories
                if len(set(row[col:col+4])) == 1 and row[col] != 0:
                    self.result = Result.P1WIN if self.turn == 1 else Result.P2WIN
                    return True
        for row in zip(*self.grid):  #Vertical victories
            for col in range(3):
                if len(set(row[col:col+4])) == 1 and row[col] != 0:
                    self.result = Result.P1WIN if self.turn == 1 else Result.P2WIN
                    return True
        for row in range(3,Connect4.ROWS):  #Diagonal victories - bottom left to top right
            for col in range(0,4):  #Only possible to 'start' these victories from the bottom left square
                if self.grid[row][col] == self.turn and self.grid[row][col] == self.grid[row-1][col+1] and self.grid[row-1][col+1] == self.grid[row-2][col+2] and self.grid[row-2][col+2] == self.grid[row-3][col+3]:
                    self.result = Result.P1WIN if self.turn == 1 else Result.P2WIN
                    return True
        for row in range(3,Connect4.ROWS):  #Diagonal victories - bottom right to top left
            for col in range(3, Connect4.COLS):   #Only possible to 'start' these victories from the bottom right square
                if self.grid[row][col] == self.turn and self.grid[row][col] == self.grid[row-1][col-1] and self.grid[row-1][col-1] == self.grid[row-2][col-2] and self.grid[row-2][col-2] == self.grid[row-3][col-3]:
                    self.result = Result.P1WIN if self.turn == 1 else Result.P2WIN
                    return True
        for i in range(Connect4.COLS):
            if self.tot[i] != Connect4.ROWS:
                self.result = Result.NONE
                return False
        self.result = Result.DRAW
        return True

    def make_move(self, move):
        """ Updates an item at a row specified by the value in the index of a column of tot, and a column specified by a column to the current turn, before incrementing the value in the index of a column of tot by +1.

        Args:
            move (int): A column in which a move is to be made on the grid
        """
        self.grid[self.tot[move]][move] = self.turn
        self.tot[move] += 1
        self.checkwin() #The game will always be unplayable after the winning move is made; function will only end after grid has been checked.
        self.change_turn()

    def undo_move(self, move):
        """ Increments the value in the index of a column of tot by -1, before updating an item at a row specified by the value in the index of a column of tot, and a column specified by a column to the zero.

        Args:
            move (int): A column in which a move is to be unmade on the grid
        """
        self.tot[move] -= 1
        self.grid[self.tot[move]][move] = 0
        self.checkwin() #The game can be updated from an unplayable state, allowing for an 'unmade' move to allow the Minimax to keep exploring depths.
        self.change_turn()

    def game_over(self):
        """ Returns True if an outcome has occurred.

        Returns:
            boolean: Whether the game has ended or not
        """
        return self.result != Result.NONE
    
    def grid_clear(self):
        """ Creates a new grid and tot, before assigning them to the class properties grid and tot.
        """
        self.grid = self.create_grid()
        self.tot = self.create_tot()
        self.result = Result.NONE
        self.turn = Connect4.P1

    def __repr__(self):
        """ Represents the grid.
        """
        for i in range(len(self.grid)):
            print(self.grid[-i-1])
