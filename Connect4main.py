import Connect4
import Connect4GUI
import MinimaxAttempt
from log_config import logging

app = Connect4GUI.App(Connect4.Connect4(7, 6), 1)
#Creates an app object with the game already instantiated, with Player 1 as the default.