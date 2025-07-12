import pyglet
import vector2D
from gui import GUI
from gameField import GameField
from physicsEngine import *

if __name__ == "__main__":
    gui_obj = GUI()
    gui_obj.physEngine.start()
    pyglet.app.run()
    
