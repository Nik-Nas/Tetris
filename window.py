from typing import Sequence

from pyglet import gl, gui
from pyglet.graphics import Batch, Group
from pyglet.window import Window

from customWidgets import CustomSlider
from graphicsTools import *


class CustomWindow(Window):

    def activate(self) -> None:
        super().activate()

    def dispatch_events(self) -> None:
        super().dispatch_events()

    def flip(self) -> None:
        super().flip()

    def get_location(self) -> tuple[int, int]:
        return super().get_location()

    def minimize(self) -> None:
        super().minimize()

    def maximize(self) -> None:
        super().maximize()

    def set_caption(self, caption: str) -> None:
        super().set_caption(caption)

    def set_location(self, x: int, y: int) -> None:
        super().set_location(x, y)

    def switch_to(self) -> None:
        super().switch_to()

    def _recreate(self, changes: Sequence[str]) -> None:
        super()._recreate(changes)

    def _create(self) -> None:
        super()._create()

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

    def delete_obj(self, *objects):
        if objects:
            for obj in objects:
                if obj in self.__windowSizedList:
                    target_list = self.__windowSizedList
                else:
                    target_list = self.__contentList
                if obj in target_list:
                    target_list.remove(obj)
                    obj.delete()
                else:

                    raise ValueError(f"object {obj} not in the list!")

    def add_obj(self, *objects, window_sized=False):
        if objects:
            if window_sized:
                target_list = self.__windowSizedList
                target_batch = self.__windowSizedContent
                target_group = self.__background
            else:
                target_list = self.__contentList
                target_batch = self.__content
                target_group = self.__foreground
            for obj in objects:
                target_list.append(obj)
                obj.batch = target_batch
                obj.group = target_group

    def add_widget(self, widget_type, widget_name, x, y, *args, events_handlers=None, **kwargs):
        if kwargs or args:
            if "batch" in kwargs: kwargs.pop("batch")
            if "group" in kwargs: kwargs.pop("group")
            widget = ""
            match widget_type:
                case WidgetType.PUSH_BUTTON:
                    widget = gui.PushButton(x, y, *args, **kwargs, batch=self.__content, group=self.__foreground)
                case WidgetType.TOGGLE_BUTTON:
                    widget = gui.ToggleButton(x, y, *args, **kwargs, batch=self.__content, group=self.__foreground)
                case WidgetType.SLIDER:
                    widget = CustomSlider(10, 100, x, y, *args, **kwargs, batch=self.__content,
                                          group=self.__foreground)
                    widget.set_handler("on_change", widget.on_change)
                case WidgetType.TEXT_ENTRY:
                    widget = gui.TextEntry(x, y, *args, **kwargs, batch=self.__content, group=self.__foreground)
            if events_handlers is not None:
                for handler in events_handlers.items():
                    widget.set_handler(handler[0], handler[1])
            self.push_handlers(widget)
            self.__widgetDict[widget_name] = widget
            return 0
        return 1

    def get_widget(self, name):
        if name and name in self.__widgetDict:
            return self.__widgetDict[name]
        raise KeyError(f"widget {name} not found")


class LinkedVar:
    def __init__(self, val):
        self.value = val


class WidgetType(enum.Enum):
    PUSH_BUTTON = 0
    TOGGLE_BUTTON = 1
    SLIDER = 2
    TEXT_ENTRY = 3
