import pyglet.window.key

import vector2
from audioManager import AudioManager
from eventManager import EventManager
from gridRasterizer import GridRasterizer
from gameField import GameField
from panel import Panel
from resourceManager import ResourceManager
from window import CustomWindow, WidgetType


class GUI:

    def on_mouse_press(self, x, y, button, modifiers):
        self._fieldRasterizer.get_cell(x, y)

    def on_key_press(self, key, modifiers):
        moved = None
        match key:
            case pyglet.window.key.SPACE:
                moved = self._field.rotate_current()
            case pyglet.window.key.LEFT:
                moved = self._field.move_current(vector2.LEFT)
            case pyglet.window.key.RIGHT:
                moved = self._field.move_current(vector2.RIGHT)
            case pyglet.window.key.DOWN:
                moved = self._field.move_current(vector2.DOWN)
        if moved: self.update_field()


    def resize_field(self, widget, value):
        self._fieldRasterizer.cell_width = int(widget.processed_value)
        self._fieldRasterizer.cell_height = int(widget.processed_value)
        self.update_field()

    def update_field(self):
        self.delete_obj(*self._sprites)
        self._panel.remove(*self._sprites)
        self._sprites = self._fieldRasterizer.to_image()
        self._panel.add(*self._sprites, relative_position=True)
        self._window.add_obj(*self._panel.children)

    def __init__(self):
        self._window = CustomWindow(resizable=True, fullscreen=False)
        self._field = GameField(20, 10)
        self._fieldRasterizer = GridRasterizer(self._field, 40, 40)
        self._resource_manager = ResourceManager("Assets")
        self._audio_manager = AudioManager(self._resource_manager)
        self._event_manager = EventManager(update_tick=1)

        self._sprites = self._fieldRasterizer.to_image()
        self._panel = Panel(200, 50)
        self._panel.add(*self._sprites, relative_position=True)
        self._window.add_obj(*self._panel.children)

        self._window.add_widget(WidgetType.SLIDER, "cellSizeSlider", 600, 400,
                                self._resource_manager.image("background"),
                                self._resource_manager.image("knob"),
                                edge=-10)
        self._window.push_handlers(self.on_key_press)
        self._window.get_widget("cellSizeSlider").set_processed_value(50)
        self._window.get_widget("cellSizeSlider").add_event_handler(self.resize_field)

        self._event_manager.add_custom_callback(self._field.tick_current)
        self._event_manager.add_custom_callback(self.update_field)

        self._event_manager.start()
        ##window show up
        self._window.set_visible()

        self._audio_manager.play_track("main_game_theme", volume=15)

    def delete_obj(self, *objects):
        self._window.delete_obj(*objects)

    def add_obj(self, *objects, window_sized=False):
        self._window.add_obj(*objects, window_sized=window_sized)

    def add_widget(self, widget_type, widget_name, x, y, *args, handlers=None, **kwargs):
        self._window.add_widget(widget_type, widget_name, x, y, *args, envents_handlers=handlers, **kwargs)
