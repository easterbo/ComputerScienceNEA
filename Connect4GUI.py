import tkinter
import random
from tkinter import ttk, Tk, Canvas, Frame, Button, Text, Radiobutton, Entry, Label, StringVar, IntVar, OptionMenu
from Connect4 import Connect4, Result
from MinimaxAttempt import Minimax
from log_config import logging


class Piece():
    """ Stores the radius of any piece placed on the grid.
    """
    R = 30


class App():
    """ Stores and represents the main window of the project as a TkInter root with class methods which allow it to be dynamic and interactive with the user. Uses a Connect4 object in order to display and play the game graphically.
    """
    WINDOW_WIDTH = 700
    WINDOW_HEIGHT = 600
    CANVAS_WIDTH = 500
    CANVAS_HEIGHT = 450
    colour = ['red', 'yellow']

    def __init__(self, game, player):
        """ Initialises the Home Screen as a TkInter root with a known Mode, Player, and Max_Depth, each of which determine the type of game the Minimax will play.

        Args:
            game (object): A predefined Connect4 object
            player (int): Either 1 or 2, deciding either which player the user is or which simulation opponent is being faced, depending on the 'mode' attribute
        """
        self.player = player
        self.mode = True
        self.root = Tk()
        self.max_depth = tkinter.IntVar()
        max_depth_options = [3, 4, 5, 6, 7]
        self.max_depth.set(max_depth_options[2])
        self.p = tkinter.IntVar()
        self.rounds = tkinter.StringVar()   #By defining these as TkInter Variables, you can easily set them using buttons on separate screens. Use .get(), .set().

        self.root.title("Connect 4")
        self.root.frame = ttk.Frame(self.root, width=App.WINDOW_WIDTH)
        self.root.frame.grid(row=0, column=0)
        self.root.text = Text(self.root.frame, bg = 'black', fg = 'white', width = 71, selectborderwidth = 1, height = 1.5, pady = 0, padx = 0)
        self.root.text.insert('1.0', "Welcome to Connect 4 with Minimax.")
        self.root.text.tag_configure("tag_name", justify='center')
        self.root.text.tag_add("tag_name", "1.0", "end")
        self.root.text.grid(row=1,column=1)
        self.root.canvas = Canvas(self.root.frame, width=App.CANVAS_WIDTH, height=App.CANVAS_HEIGHT)
        self.root.canvas.grid(row=2, column=1)
        self.root.canvas.bind('<Button-1>', self.canvas_click)
        self.root.buttonholder = ttk.Frame(self.root, width=App.WINDOW_WIDTH)
        self.root.buttonholder.grid(row = 3, column = 0)
        self.root.button1 = Button(self.root.buttonholder, text = 'New Game', activebackground = 'yellow', bg = 'grey', command = self.player_select_screen, height = 1, justify = 'center', width = 8, padx = 30)
        self.root.button1.pack(side = "left")
        self.root.dropdown = OptionMenu(self.root.buttonholder, self.max_depth, *max_depth_options)
        self.root.dropdown.pack(side = "right")
        self.root.description = Label(self.root.buttonholder, text = 'Minimax Depth:')
        self.root.description.pack(side = "right", padx = (10,0))
        self.root.button2 = Button(self.root.buttonholder, text = 'Simulation', activebackground = 'yellow', bg = 'grey', command = self.s_player_select_screen, height = 1, justify = 'center', width = 8, padx = 30)
        self.root.button2.pack(side = "right")

        self.new_game(game)

        self.draw()
        self.root.mainloop()    

    def draw(self):
        """ Clears the canvas in the centre of the window, before drawing the grid and current pieces on top of it.
        """
        self.root.canvas.delete('all')
        self.draw_grid()
        self.draw_pieces()
    
    def new_game(self, game):
        """ Creates a new game and sets it to the class property.

        Args:
            game (object): A predefined Connect4 object
        """
        assert type(game) == Connect4 and game is not None
        self.game = game
    
    def delay(self, function):
        """ Runs a function after a 100ms rest without running any other lines of code before the function has been completed. This is here due to the after() function in TkInter continuing to run further lines in the code despite the initial intended function not having been run yet

        Args:
            function (function): Any function
        """
        self.root.after(100, function)  #Use whenever 'animating' Minimax.

    def final_result(self):
        """ Updates the text display above the grid to a message either indicating which player has won the game, or whether the game was a draw
        """
        self.root.text.delete('1.0', '100.0')
        if self.game.result == Result.P1WIN:
            self.root.text.insert('1.0', f'Player 1 Wins!')
            self.root.text.tag_add("tag_name", "1.0", "end")
        if self.game.result == Result.P2WIN:
            self.root.text.insert('1.0', f'Player 2 Wins!')
            self.root.text.tag_add("tag_name", "1.0", "end")
        if self.game.result == Result.DRAW:
            self.root.text.insert('1.0', f'DRAW!')
            self.root.text.tag_add("tag_name", "1.0", "end")

    def s_final_result(self, win_count_minimax, win_count_opponent):
        """ Updates the running total scores for the Minimax algorithm and it’s opponent during a simulation, drawing them each in the text display above the grid, before returning them.

        Args:
            win_count_minimax (double): The current number of victories achieved by the Minimax function (draws are counted as half a win)
            win_count_opponent (double): The current number of victories achieved by the opponent function (draws are counted as half a win)

        Returns:
            tuple: both scores updated in accordance to the outcome achieved
        """
        if self.game.result == Result.P1WIN:
            win_count_minimax += 1
        elif self.game.result == Result.P2WIN:
            win_count_opponent += 1
        elif self.game.result == Result.DRAW:
            win_count_minimax += 0.5
            win_count_opponent += 0.5
        self.root.text.delete('1.0', '100.0')
        self.root.text.insert('1.0', f'Minimax: {win_count_minimax}     Opponent: {win_count_opponent}')
        self.root.text.tag_add("tag_name", "1.0", "end")
        self.game.grid_clear()
        self.game.change_turn()
        return win_count_minimax, win_count_opponent    #Due to draws, this is a 'double' data type tuple.
    
    def canvas_click(self, event):
        """ If the canvas is clicked on, this function checks whether it is an ongoing game, the player’s turn, and a game, rather than a simulation. If true, then the x-co-ordinates of the click are calculated to find which column the click took place in. If valid, a counter is played at the correct height in the column, otherwise ‘That column is full.’ is displayed in a text box and no move is made.

        Args:
            event (object): Stores attributes about a click that occured on a canvas on a canvas
        """
        if not self.game.game_over() and self.game.turn == self.player and self.mode == True: 
            if 0 < event.x < App.CANVAS_WIDTH and 0 < event.y < App.CANVAS_HEIGHT:
                move = self.find_column(event.x)
                if self.game.valid_move(move):
                    self.game.make_move(move)
                    self.draw()
                    self.root.update_idletasks()    #Updates the grid while the game is still being played, rather than after Minimax plays.
                    if self.game.game_over():
                        self.final_result()
                    else:
                        self.root.text.delete('1.0', '100.0')
                        self.root.text.insert('1.0', 'Minimax thinking...')
                        self.root.text.tag_add("tag_name", "1.0", "end")
                        self.root.update_idletasks()
                        self.root.after(500, self.min_max_move(self.max_depth.get()))
                        self.root.text.delete('1.0', '100.0')
                        self.draw()
                        if self.game.game_over():
                            self.final_result()
                else:
                    self.root.text.delete('1.0', '100.0')
                    self.root.text.insert('1.0', 'That column is full.')
                    self.root.text.tag_add("tag_name", "1.0", "end")

    
    def simulation(self, win_count_minimax, win_count_opponent):
        """ Decides which opponent the minimax algorithm is facing, before playing a game of them against one another, checking whether a win has been achieved every turn. If so, then final_result is called, and if not, the function is called recursively. If the maximum number of rounds has been played, the text box changes from the scores of each player, being prepended with ‘Final score:’.

        Args:
            win_count_minimax (double): The current number of victories achieved by the Minimax function (draws are counted as half a win)
            win_count_opponent (double): The current number of victories achieved by the opponent function (draws are counted as half a win)
        """
        self.root.text.delete('1.0', '100.0')
        self.root.text.insert('1.0', f'Minimax: {win_count_minimax}    Opponent: {win_count_opponent}')
        self.root.text.tag_add("tag_name", "1.0", "end")
        if win_count_minimax + win_count_opponent != self.rounds:
            if self.player == 1:    #self.player remains SEPARATE from self.turn, therefore this can stay
                self.delay(self.min_max_move(self.max_depth.get())) if self.game.turn == self.game.P1 else self.delay(self.random_move())
            else:
                self.delay(self.min_max_move(self.max_depth.get())) if self.game.turn == self.game.P1 else self.delay(self.min_max_move(self.player+1))
            if self.game.game_over():
                win_count_minimax, win_count_opponent = self.s_final_result(win_count_minimax, win_count_opponent)
            self.draw()
            self.root.update_idletasks() 
            
            self.simulation(win_count_minimax, win_count_opponent)
        else:
            self.root.text.insert('1.0', 'Final Result: ')
            self.root.text.tag_add("tag_name", "1.0", "end")
            self.rounds = tkinter.StringVar()   #Otherwise .get() and .set() do not work on a second simulation

    def random_move(self):
        """ Makes a random, valid move.
        """
        if not self.game.game_over():
            move = random.randint(0,6)
            while self.game.valid_move(move) == False:
                move = random.randint(0,6)
            self.game.make_move(move)

    def min_max_move(self, max_depth):
        """ Creates a Minimax object and calls minimax on the current grid with a max depth, making a move in the column returned.

        Args:
            max_depth (int): The maximum 'depth' that the Minimax object can explore, or the maximum number of moves that can be made on the grid by the Minimax object
        """
        if not self.game.game_over():
            minimax = Minimax(self.game)
            minimax.minimax(0, max_depth, self.game.turn)
            if self.game.valid_move(minimax.best_move):
                self.game.make_move(minimax.best_move)
            else:   
                self.random_move()
        
    
    def draw_grid(self):
        """ Draws lines over the canvas at equal intervals to create a grid.
        """
        for i in range(0, App.CANVAS_WIDTH, App.CANVAS_WIDTH // Connect4.COLS):
            self.root.canvas.create_line(i, 0, i, App.CANVAS_HEIGHT)
        for i in range(0, App.CANVAS_HEIGHT, App.CANVAS_HEIGHT // Connect4.ROWS):
            self.root.canvas.create_line(0, i, App.CANVAS_WIDTH, i)

    def draw_pieces(self):
        """ Draws circles at each point in the grid where specified by the game object, the colour corresponding to each player.
        """
        grid = self.game.return_grid()[::-1]
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] != 0:
                    self.colour = App.colour[0] if grid[row][col] == Connect4.P1 else App.colour[1]
                    COL_WIDTH = App.CANVAS_WIDTH // Connect4.COLS
                    ROW_HEIGHT = App.CANVAS_HEIGHT // Connect4.ROWS
                    self.circle((COL_WIDTH*col) + (COL_WIDTH // 2), (ROW_HEIGHT*row) + (ROW_HEIGHT // 2))

    def find_column(self, x):
        """ Calculates the column at which an x co-ordinate is within.

        Args:
            x (double): The x co-ordinate along the canvas at which a click occured

        Returns:
            double: The column in which the canvas was clicked
        """
        return x // (App.CANVAS_WIDTH // Connect4.COLS)

    def circle(self, x, y):
        """ Draws a circle at an x and y co-ordinate, with radius r.

        Args:
            x (double): The x co-ordinate along the canvas at which a click occured
            y (double): The y co-ordinate along the canvas at which a click occured
        """
        xl = x - Piece.R
        yl = y - Piece.R
        xr = x + Piece.R
        yr = y + Piece.R
        self.root.canvas.create_oval(xl, yl, xr, yr, fill=self.colour)

    def return_to_game(self, mode):
        """ Updates whether the game is a simulation or active game, clears the grid, sets the player, and begins either a simulation, or a game, updating the text display to reflect this.

        Args:
            mode (boolean): False if the new game is a simulation, True otherwise
        """
        self.mode = mode
        self.game.grid_clear()
        self.draw()
        self.player = int(self.p.get())
        if self.mode == True:
            self.root.text.delete('1.0', '100.0')
            self.root.text.insert('1.0', "Welcome to Connect 4 with Minimax.")
            self.root.text.tag_configure("tag_name", justify='center')
            self.root.text.tag_add("tag_name", "1.0", "end")
            if self.player == self.game.P2:
                self.root.after(1000, self.min_max_move(self.max_depth.get()))
                self.draw()
        else:
            self.game.turn = self.game.P1
            self.rounds = int(self.rounds.get()) if self.rounds.get().isdigit() else 10     #Rounds validation
            if self.rounds < 1 or self.rounds > 50:                                         #Also rounds validation
                self.rounds = 10
            self.root.after(2000, self.simulation(0,0))

    def player_select_screen(self):
        """ When the ‘New Game’ button is pressed, a new window is created with a text display, two radiobuttons and an Enter button, where the player can select which player they want to be in the new game.
        """
        player_select_screen = tkinter.Toplevel(self.root)
        player_select_screen.title("Player Select Screen")
        player_select_screen.frame = ttk.Frame(player_select_screen, width=App.WINDOW_WIDTH)
        player_select_screen.frame.grid(row=0, column=0)
        player_select_screen.text = Text(player_select_screen.frame, bg = 'grey', fg = 'black', width = 21, selectborderwidth = 1, height = 1.5, pady = 0, padx = 0)
        player_select_screen.text.insert('1.0', "Would you like to be Player 1 or Player 2?")
        player_select_screen.text.tag_configure("tag_name", justify='center')
        player_select_screen.text.tag_add("tag_name", "1.0", "end")
        player_select_screen.text.grid(row=1,column=1)
        player_select_screen.player_choice1 = Radiobutton(player_select_screen.frame, text = 'Player 1', bg = 'grey', variable = self.p, value = 1, command = self.p.set(1), height = 1, justify = 'center', width = 10)
        player_select_screen.player_choice2 = Radiobutton(player_select_screen.frame, text = 'Player 2', bg = 'grey', variable = self.p, value = 2, command = self.p.set(2), height = 1, justify = 'center', width = 10)
        player_select_screen.player_choice1.grid(row=2,column=1)
        player_select_screen.player_choice2.grid(row=3,column=1)
        player_select_screen.enter = Button(player_select_screen.frame, text = 'ENTER', bg = 'grey', command = lambda: [player_select_screen.destroy(), self.return_to_game(True)], height = 1, justify = 'center', width = 10)
        player_select_screen.enter.grid(row=4,column=1)
        player_select_screen.mainloop()

    def s_player_select_screen(self):
        """ When the ‘Simulation’ button is pressed, a new window is created with a text display, two radiobuttons, an entry box and an Enter button, where the player can select which opponent they want their minimax to face, and for how many rounds.
        """
        s_player_select_screen = tkinter.Toplevel(self.root)
        s_player_select_screen.title("Simulation Player Select Screen")
        s_player_select_screen.frame = ttk.Frame(s_player_select_screen, width=App.WINDOW_WIDTH)
        s_player_select_screen.frame.grid(row=0, column=0)
        s_player_select_screen.text = Text(s_player_select_screen.frame, bg = 'grey', fg = 'black', width = 50, selectborderwidth = 1, height = 1.5, pady = 0, padx = 0)
        s_player_select_screen.text.insert('1.0', "Minimax Player vs Who?")
        s_player_select_screen.text.tag_configure("tag_name", justify='center')
        s_player_select_screen.text.tag_add("tag_name", "1.0", "end")
        s_player_select_screen.text.grid(row=1,column=1)
        s_player_select_screen.player_choice1 = Radiobutton(s_player_select_screen.frame, text = 'Random Player', bg = 'grey', variable = self.p, command = self.p.set(1), value= 1, height = 1)
        s_player_select_screen.player_choice2 = Radiobutton(s_player_select_screen.frame, text = 'Minimax Player: Depth 3', bg = 'grey', variable = self.p, command = self.p.set(2), value= 2, height = 1)
        s_player_select_screen.player_choice3 = Radiobutton(s_player_select_screen.frame, text = 'Minimax Player: Depth 4', bg = 'grey', variable = self.p, command = self.p.set(3), value= 3, height = 1)
        s_player_select_screen.player_choice4 = Radiobutton(s_player_select_screen.frame, text = 'Minimax Player: Depth 5', bg = 'grey', variable = self.p, command = self.p.set(4), value= 4, height = 1)
        s_player_select_screen.player_choice5 = Radiobutton(s_player_select_screen.frame, text = 'Minimax Player: Depth 6', bg = 'grey', variable = self.p, command = self.p.set(5), value= 5, height = 1)
        s_player_select_screen.player_choice6 = Radiobutton(s_player_select_screen.frame, text = 'Minimax Player: Depth 7', bg = 'grey', variable = self.p, command = self.p.set(6), value= 6, height = 1)
        s_player_select_screen.round_entry_label = Label(s_player_select_screen.frame, anchor = 'w', bg = 'grey', text = 'Enter the number of rounds you wish to see (1 - 50): \n (Anything out of range will default to 10)')
        s_player_select_screen.round_entry = Entry(s_player_select_screen.frame, bg = 'white', textvariable = self.rounds)
        s_player_select_screen.player_choice1.grid(row=2,column=1)
        s_player_select_screen.player_choice2.grid(row=3,column=1)
        s_player_select_screen.player_choice3.grid(row=4,column=1)
        s_player_select_screen.player_choice4.grid(row=5,column=1)
        s_player_select_screen.player_choice5.grid(row=6,column=1)
        s_player_select_screen.player_choice6.grid(row=7,column=1)
        s_player_select_screen.round_entry_label.grid(row=8,column=1)
        s_player_select_screen.round_entry.grid(row=9,column=1)
        s_player_select_screen.enter = Button(s_player_select_screen.frame, text = 'ENTER', bg = 'grey', command = lambda: [s_player_select_screen.destroy(), self.return_to_game(False)], height = 1, justify = 'center', width = 10)
        s_player_select_screen.enter.grid(row=10,column=1)
        s_player_select_screen.mainloop()