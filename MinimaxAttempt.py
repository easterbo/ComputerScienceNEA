from Connect4 import Connect4, Result
from time import time
import math
import random
from log_config import logging

class Minimax:
    """ Stores the best move, initially a random move, to be made on a Connect4 game. Has class methods allowing it to calculate the best move via evaluating the grid in terms of positive and negative score.
    """

    def __init__(self, game):
        """ Initialises the Minimax object with the current game and assigns a random column as the best move.

        Args:
            game (object): The current game object 
        """
        self.game = game
        self.best_move = random.randint(0,6)

    def minimax(self, depth, max_depth, maximising_player):
        """ Returns a positive infinity, negative infinity, or 0 value depending on whether the game has reached a result, or the heuristic score of the game state if the maximum depth has been reached. Otherwise, it calculates all possible moves on the game state and makes them until these conditions have been met. Once they have, the movements are evaluated, either by comparing game state to a table of values as to create a heuristic 'score' for each move, negative for the opponent, positive for the plauer, or by a very high, very low, or average score for a win, loss and draw respectively. These scores for each move are compared to find the highest score-available move, which is then assigned to a class variable. 

        Args:
            depth (int): The current 'depth' the Minimax is operating at, or how many turns have been taken total by the Minimax
            max_depth (int): The maximum 'depth' at which the Minimax is allowed to explore, or how many turns the Minimax is able to take
            maximising_player (int): The player whose point of view the Minimax is operating from

        Returns:
            int: Either a 0, 500, or -500 if an outcome has occured, respective of the outcome. Otherwise, an integer calculated by the evaluation function when given the grid. Once all nodes have been explored, however, the highest score achieved by either method is returned
        """
        if self.game.game_over():   #Outcome
            if self.game.result != Result.DRAW:
                res = 1 if self.game.result == Result.P1WIN else 2
                return 500 if res == maximising_player else -500
            else:
                return 0

        elif depth == max_depth:    #Max depth
            return self.evaluation(self.game.grid, maximising_player)

        else:   #Otherwise
            best_score = -500 if maximising_player == self.game.turn else 500
            for i in range(self.game.COLS):
                if self.game.valid_move(i):
                    self.game.make_move(i)
                    score = self.minimax(depth+1, max_depth, maximising_player)    #Recursive call, consider as changing turn and making another move
                    self.game.undo_move(i)  #End of recursive call, -1 step.
                    if maximising_player == self.game.turn:
                        if score > best_score:
                            best_score = score
                            if depth == 0:
                                self.best_move = i
                    else:
                        if score < best_score:
                            best_score = score
                            if depth == 0:
                                self.best_move = i
                    
            return best_score

    def random_move(self):
        """ Returns a random integer between zero and the number of columns in the grid.

        Returns:
            int: A random integer between zero and the number of columns in the grid
        """
        best_col = random.randint(0, self.game.COLS)
        return best_col

    def evaluation(self, grid, maximising_player):
        """ Assigns a total positive and negative score to the current grid depending on where the maximising player and opponent's pieces are compared to the values stored within a table.

        Args:
            grid (2D Array): The grid of the game object with any number of moves made onto it by the Minimax object
            maximising_player (int): The player whose counter positions will be counted as positive

        Returns:
            int: The evaluation heuristic of the grid fed into the function from the point of view of the maximising player
        """
        positions = [
        [ 3, 4, 5, 7, 5, 4, 3], 
        [ 4, 6, 8,10, 8, 6, 4], 
        [ 5, 8,11,13,11, 8, 5], 
        [ 5, 8,11,13,11, 8, 5],
        [ 4, 6, 8,10, 8, 6, 4], 
        [ 3, 4, 5, 7, 5, 4, 3]
        ]
        
        player_score = opponent_score = 0

        positions = [score for row in positions for score in row]
        grid = [piece for row in grid for piece in row]

        for i in range(len(positions)):
            if grid[i] == maximising_player:
                player_score += positions[i]
            if grid[i] != 0 and grid[i] != maximising_player:
                opponent_score += positions[i]
            
        return player_score - opponent_score
    
