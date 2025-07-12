import pyglet.window.key
from pyglet import resource

from fieldRasterizer import *
from window import CustomWindow, WidgetType


class GUI:

    def on_mouse_press(self, x, y, button, modifiers):
        self.__fieldRasterizer.getCell(x, y)


    def on_key_press(self, key, modifiers):
        if key == pyglet.window.key.SPACE:
            self.__field.rotate_current()
            self.update_field()


    def resize_field(self, widget, value):
            self.__window.delete(*self.__sprites)
            self.__fieldRasterizer.cell_width = int(widget._processed_value)
            self.__fieldRasterizer.cell_height = int(widget._processed_value)
            self.__sprites = self.__fieldRasterizer.toImage()
            self.__window.add(*self.__sprites)

    def update_field(self):
        self.__window.delete(*self.__sprites)
        self.__sprites = self.__fieldRasterizer.toImage()
        self.__window.add(*self.__sprites)
            
    def __init__(self):
        self.__window = CustomWindow(resizable=True, fullscreen=False)
        self.__field = GameField(20, 10)
        self.__fieldRasterizer = FieldRasterizer(self.__field, 60, 60)
        self.__sprites = self.__fieldRasterizer.toImage()
        self.__window.add(*self.__sprites)
        self.__window.addWidget(WidgetType.SLIDER, "cellSizeSlider", 600, 400,
                                resource.image("Assets/background.png"),
                                resource.image("Assets/knob.png"),
                                edge=-10)
        self.__window.push_handlers(self.on_key_press)
        self.__window.getWidget("cellSizeSlider").set_processed_value(60)
        self.__window.getWidget("cellSizeSlider").add_event_handler(self.resize_field)

        self.physEngine = PhysicsEngine(gravity=vector2D.Vector2D(0, -1), update_tick=0.5)
        self.physEngine.add_custom_callback(self.update_field)
        self.physEngine.add_custom_callback(self.__field.tick_current)
    
        ##window show up
        self.__window.set_visible()


    def delete(self, *objects):
        if objects:
            self.__window.delete(*objects)


    def add(self, *objects, window_sized=False):
        if objects:
            self.__window.add(*objects, windowSized=window_sized)

    def addWidget(self, widget_type, widget_name, x, y, *args, handlers=None, **kwargs):
        if kwargs or args:
            self.__window.addWidget(widget_type, widget_name, x, y, *args, envents_handlers=handlers, **kwargs)














        
