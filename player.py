from python import Python
from config import *

def create_player1():
    return Python(5, 5, BLUE, PLAYER_1_KEYS)

def create_player2():
    return Python(GRID_WIDTH - 6, GRID_HEIGHT - 6, YELLOW, PLAYER_2_KEYS)
