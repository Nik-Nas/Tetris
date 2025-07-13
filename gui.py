import pyglet.window.key
from pyglet import resource
from gameField import GameField
from physicsEngine import PhysicsEngine
from fieldRasterizer import *
from resourceManager import ResourceManager
from vector2D import Vector2D
from window import CustomWindow, WidgetType


class GUI:

    def on_mouse_press(self, x, y, button, modifiers):
        self.__fieldRasterizer.get_cell(x, y)

    def on_key_press(self, key, modifiers):
        if key == pyglet.window.key.SPACE:
            self.__field.rotate_current()
            self.update_field()

    def resize_field(self, widget, value):
        self.__fieldRasterizer.cell_width = int(widget.processed_value)
        self.__fieldRasterizer.cell_height = int(widget.processed_value)
        self.update_field()

    def update_field(self):
        self.delete_obj(*self.__sprites)
        self.__sprites = self.__fieldRasterizer.to_image()
        self.add_obj(*self.__sprites)

    def __init__(self):
        self.__window = CustomWindow(resizable=True, fullscreen=False)
        self.__field = GameField(20, 10)
        self.__fieldRasterizer = FieldRasterizer(self.__field, 60, 60)
        self.__resource_manager = ResourceManager("Assets")
        self.__sprites = self.__fieldRasterizer.to_image()
        self.__window.add_obj(*self.__sprites)
        self.__window.add_widget(WidgetType.SLIDER, "cellSizeSlider", 600, 400,
                                 self.__resource_manager.get("background"),
                                 self.__resource_manager.get("knob"),
                                 edge=-10)
        self.__window.push_handlers(self.on_key_press)
        self.__window.get_widget("cellSizeSlider").set_processed_value(60)
        self.__window.get_widget("cellSizeSlider").add_event_handler(self.resize_field)

        self.physEngine = PhysicsEngine(gravity=Vector2D(0, -1), update_tick=0.5)
        self.physEngine.add_custom_callback(self.update_field)
        self.physEngine.add_custom_callback(self.__field.tick_current)

        ##window show up
        self.__window.set_visible()

    def delete_obj(self, *objects):
        self.__window.delete_obj(*objects)

    def add_obj(self, *objects, window_sized=False):
        self.__window.add_obj(*objects, window_sized=window_sized)

    def add_widget(self, widget_type, widget_name, x, y, *args, handlers=None, **kwargs):
        self.__window.add_widget(widget_type, widget_name, x, y, *args, envents_handlers=handlers, **kwargs)
