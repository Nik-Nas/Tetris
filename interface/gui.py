import pyglet.window.key

from drawing.gridRasterizer import GridRasterizer
from gameplay.gameField import GameField
from interface.panel import Panel
from interface.window import CustomWindow
from tools import vector2
from tools.audioManager import AudioManager
from tools.eventManager import EventManager
from tools.resourceManager import ResourceManager


class GUI:

    def on_mouse_press(self, x, y, button, modifiers):
        self._field_rasterizer.get_cell(x, y)

    def on_key_press(self, key, modifiers):
        moved = None
        match key:
            case pyglet.window.key.UP:
                moved = self._field.rotate_current()
            case pyglet.window.key.SPACE:
                moved = self._field.hard_drop()
            case pyglet.window.key.LEFT:
                moved = self._field.move_current(vector2.LEFT)
            case pyglet.window.key.RIGHT:
                moved = self._field.move_current(vector2.RIGHT)
            case pyglet.window.key.DOWN:
                moved = self._field.move_current(vector2.DOWN)
        if moved:
            self.update_field()


    def resize_field(self, widget, value):
        self._field_rasterizer.cell_width = int(widget.processed_value)
        self._field_rasterizer.cell_height = int(widget.processed_value)
        self.update_field()

    def update_field(self):
        self.label.text = str(self._field.score)
        self.delete_obj(*self._sprites)
        self._panel.remove(*self._sprites)
        self._sprites = self._field_rasterizer.to_image()
        self._panel.add(*self._sprites, relative_position=True)
        self._window.add_obj(*self._panel.children, layer=1)

    def __init__(self):
        self._window = CustomWindow(resizable=False, fullscreen=False)
        self._field = GameField(20, 10)
        self._window.set_size(500, 700)
        self._field_rasterizer = GridRasterizer(self._field, 30, 30)

        self._next_piece_rasterizer = GridRasterizer(self._field, 30, 30)

        self._resource_manager = ResourceManager("Assets")
        self._audio_manager = AudioManager(self._resource_manager)
        self._event_manager = EventManager(update_tick=1)

        self._sprites = self._field_rasterizer.to_image()
        self._panel = Panel(25, 25)
        self._panel.add(*self._sprites, relative_position=True)
        self._window.push_handlers(self.on_key_press)

        self.label = pyglet.text.Label(str(self._field.score), font_name='Arial', font_size=30,
                                  x=425, y=200, color=(0, 0, 0),
                                  anchor_x='right', anchor_y='top')

        self.label_1 = pyglet.text.Label("GAME OVER", font_name='Arial', font_size=30,
                                    x=125, y=370, color=(0, 0, 0))
        self.label_1.visible = False
        self.bckgr = pyglet.shapes.Rectangle(x=125, y=365, color=(240, 240, 240), width=250, height=50)
        self.bckgr.opacity = 255
        self.bckgr.visible = False

        ind = self._window.add_layer()

        self._window.add_obj(self.bckgr,   layer=ind)
        self._window.add_obj(self.label_1, layer=ind)

        self._panel.add(self.label, relative_position=True)
        self._window.add_obj(*self._panel.children, layer=1)
        del ind
        self._field.push_handlers(self.on_game_over)

        self._event_manager.add_custom_callback(self._field.tick_current)
        self._event_manager.add_custom_callback(self.update_field)

        self._event_manager.start()
        ##window show up
        self._window.set_visible()
        self._audio_manager.play_track("main_game_theme", volume=0)

    def delete_obj(self, *objects):
        self._window.delete_obj(*objects)

    def add_obj(self, *objects, layer: int):
        self._window.add_obj(*objects, layer=layer)

    def add_widget(self, widget_type, widget_name, x, y, *args, handlers=None, **kwargs):
        self._window.add_widget(widget_type, widget_name, x, y, *args, envents_handlers=handlers, **kwargs)


    def on_game_over(self):
        self._window.pop_handlers()
        self._event_manager.stop()
        self.bckgr.visible = True
        self.label_1.visible = True
