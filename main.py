from gui import GUI
from physicsEngine import *

if __name__ == "__main__":
    gui_obj = GUI()
    gui_obj.physEngine.start()
    pyglet.app.run()
    
