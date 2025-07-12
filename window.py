from enum import Enum
from pyglet.gui import Slider
from pyglet.window import Window
from pyglet import resource
from pyglet.graphics import Batch, Group
from pyglet.shapes import Rectangle, Line
from pyglet import gl
from gameField import GameField
from eventManager import EventManager
from pixelMathTools import *
from customWidgets import CustomSlider  
from graphicsTools import *

class CustomWindow (Window):



    def on_draw(self):
        self.clear()
        self.__windowSizedContent.draw()
        self.__content.draw()


    def on_resize(self, width, height):
        super().on_resize(width, height)
        for sprite in self.__windowSizedList:
            sprite.width = width
            sprite.height = height


    def __init__(self, *args, **kwargs):
        if "visible" not in kwargs: kwargs["visible"] = False
        super().__init__(*args, **kwargs)
        
        # creating rendering batch for drawable stuff
        self.__windowSizedContent = Batch()
        self.__content = Batch()
        self.__widgets = Batch()
        self.__windowSizedList = []
        self.__contentList = []
        self.__widgetDict = {}


        # create rendering groups to differentiate between foreground and background
        self.__foreground = Group(order=1)
        self.__background = Group(order=0)
        # epic initialization ends here


        # epic window setup starts here
        self.set_minimum_size(500, 500)
        background_color = [1, 1, 1, 1]
        gl.glClearColor(*background_color)

##        self.push_handlers(self.on_draw, self.on_resize)
        
##        self.__gui = GUI()
##        self.__eventManager = EventManager()
        ##epic initialization starts here
##        self.__cs = 70

        ##creating game field
##        self.__field = GameField(10, 10)
##        self.__gui.add(Rectangle(0, 0, self.__gui._windowSize[0], \
##                                 self.__gui._windowSize[1], (255, 255, 255)),\
##                       windowSized=True)
##        self.__gui.add(*self.__field.toImage(self.__cs, self.__cs))
##        self.__gui.addWidget(WidgetType.SLIDER, "cellSizeSlider", 600, 400, \
##                             resource.image("background.png"), \
##                             resource.image("knob.png"), \
##                             edge=-10)
        
        
    def delete(self, *objects):
        if objects:
            for obj in objects:
                if obj in self.__windowSizedList:
                    targetList = self.__windowSizedList
                else:
                    targetList = self.__contentList
                if obj in targetList:
                    targetList.remove(obj)
                    obj.delete()
                else: raise ValueError(f"object {obj} not in the list!")


    def add(self, *objects, windowSized=False):
        if objects:
            if windowSized:
                targetList = self.__windowSizedList
                targetBatch = self.__windowSizedContent
                targetGroup = self.__background
            else:
                targetList = self.__contentList
                targetBatch = self.__content
                targetGroup = self.__foreground
            for obj in objects:
                targetList.append(obj)
                obj.batch = targetBatch
                obj.group = targetGroup


    def addWidget(self, widgetType, widgetName, x, y, *args, events_handlers=None, **kwargs):
        if kwargs or args:
            if "batch" in kwargs: kwargs.pop("batch")
            if "group" in kwargs: kwargs.pop("group")
            widget = ""
            match widgetType:
                case WidgetType.PUSH_BUTTON:
                    widget = gui.PushButton(x, y, *args, **kwargs, batch=self.__content, \
                                            group=self.__foreground)
                case WidgetType.TOGGLE_BUTTON:
                    widget = gui.ToggleButton(x, y, *args, **kwargs, batch=self.__content, \
                                            group=self.__foreground)
                case WidgetType.SLIDER:
                    widget = CustomSlider(10, 100, x, y, *args, **kwargs, batch=self.__content, \
                                            group=self.__foreground)
                    widget.set_handler("on_change", widget.on_change)
                case WidgetType.TEXT_ENTRY:
                    widget = gui.TextEntry(x, y, *args, **kwargs, batch=self.__content, \
                                            group=self.__foreground)
            if events_handlers is not None:
                for handler in events_handlers.items():
                    widget.set_handler(handler[0], handler[1])
            self.push_handlers(widget)
            self.__widgetDict[widgetName] = widget
            return 0
        return 1

    def getWidget(self, name):
        if name and name in self.__widgetDict:
            return self.__widgetDict[name]

class LinkedVar:
    def __init__(self, val):
        self.value = val


class WidgetType(Enum):
    PUSH_BUTTON = 0
    TOGGLE_BUTTON = 1
    SLIDER = 2
    TEXT_ENTRY = 3






