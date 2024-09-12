from enum import Enum

class Result(Enum):
    NONE = 0
    P1WIN = 1
    P2WIN = 2
    DRAW = 3

class Connect4:
    P1 = 1
    P2 = 2
    COLS = 0
    ROWS = 0

    def __init__(self, COLS, ROWS):
        Connect4.COLS = COLS
        Connect4.ROWS = ROWS
        self.grid = self.create_grid()
        self.tot = self.create_tot()
        self.turn = Connect4.P1
        self.result = Result.NONE

    def create_grid(self):
        grid = []
        for i in range(Connect4.ROWS):
            grid.append([])
            for j in range(Connect4.COLS):
                grid[i].append(0)
        return grid

    def return_grid(self):
        return self.grid
    
    def create_tot(self):
        tot = []
        for i in range(Connect4.COLS):
            tot.append(0)
        return tot

    def valid_move(self, move):
        if self.tot[move] == Connect4.ROWS or move > Connect4.COLS-1 or move < 0:
            return False
        return True
    
    def change_turn(self):
        self.turn = Connect4.P2 if self.turn == Connect4.P1 else Connect4.P1

    def checkwin(self):
        for row in self.grid:
            for col in range(Connect4.COLS-3):  #Horizontal
                if len(set(row[col:col+4])) == 1 and row[col] != 0:
                    self.result = Result.P1WIN if self.turn == 1 else Result.P2WIN
                    return True
        for row in zip(*self.grid): #Vertical
            for col in range(3):
                if len(set(row[col:col+4])) == 1 and row[col] != 0:
                    self.result = Result.P1WIN if self.turn == 1 else Result.P2WIN
                    return True
        for row in range(3,Connect4.ROWS):  #Diagonal
            for col in range(0,4):
                if self.grid[row][col] == self.turn and self.grid[row][col] == self.grid[row-1][col+1] and self.grid[row-1][col+1] == self.grid[row-2][col+2] and self.grid[row-2][col+2] == self.grid[row-3][col+3]:
                    self.result = Result.P1WIN if self.turn == 1 else Result.P2WIN
                    return True
        for row in range(3,Connect4.ROWS):
            for col in range(3, Connect4.COLS):
                if self.grid[row][col] == self.turn and self.grid[row][col] == self.grid[row-1][col-1] and self.grid[row-1][col-1] == self.grid[row-2][col-2] and self.grid[row-2][col-2] == self.grid[row-3][col-3]:
                    self.result = Result.P1WIN if self.turn == 1 else Result.P2WIN
                    return True
        if all(self.tot) == Connect4.ROWS:
            self.result = Result.DRAW
            return True
        return False
    
    def make_move(self, move):
        self.grid[self.tot[move]][move] = self.turn
        self.tot[move] += 1
        self.change_turn()
    
    def undo_move(self, move):
        self.tot[move] -= 1
        self.grid[self.tot[move]][move] = 0
        self.change_turn()

    def game_over(self):
        return self.result != Result.NONE
    
    def grid_clear(self):
        self.grid = self.create_grid()
        self.tot = self.create_tot()
        self.result = Result.NONE
        self.turn = Connect4.P1

    def __repr__(self):
        for i in range(len(self.grid)):
            print(self.grid[-i-1])
