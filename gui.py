import pyglet.window.key

from audioManager import AudioManager
from eventManager import EventManager
from fieldRasterizer import FieldRasterizer
from gameField import GameField
from resourceManager import ResourceManager
from vector2D import Vector2dPresets
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
                moved = self._field.move_current(Vector2dPresets.LEFT)
            case pyglet.window.key.RIGHT:
                moved = self._field.move_current(Vector2dPresets.RIGHT)
            case pyglet.window.key.DOWN:
                moved = self._field.move_current(Vector2dPresets.DOWN)
        if moved: self.update_field()


    def resize_field(self, widget, value):
        self._fieldRasterizer.cell_width = int(widget.processed_value)
        self._fieldRasterizer.cell_height = int(widget.processed_value)
        self.update_field()

    def update_field(self):
        self.delete_obj(*self._sprites)
        self._sprites = self._fieldRasterizer.to_image()
        self.add_obj(*self._sprites)

    def __init__(self):
        self._window = CustomWindow(resizable=True, fullscreen=False)
        self._field = GameField(10, 10)
        self._fieldRasterizer = FieldRasterizer(self._field, 60, 60)
        self._resource_manager = ResourceManager("Assets")
        self._audio_manager = AudioManager(self._resource_manager)
        self._sprites = self._fieldRasterizer.to_image()
        self._window.add_obj(*self._sprites)
        self._window.add_widget(WidgetType.SLIDER, "cellSizeSlider", 600, 400,
                                self._resource_manager.image("background"),
                                self._resource_manager.image("knob"),
                                edge=-10)
        self._window.push_handlers(self.on_key_press)
        self._window.get_widget("cellSizeSlider").set_processed_value(60)
        self._window.get_widget("cellSizeSlider").add_event_handler(self.resize_field)

        self._event_manager = EventManager(update_tick=1)

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
