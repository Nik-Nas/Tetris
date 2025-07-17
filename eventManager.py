import time
from typing import Callable

import pyglet.clock


class EventManager:

    def __init__(self, update_tick: float, gravity=None):
        if gravity is not None:
            self.__gravity_force = gravity.length
        else:
            self.__gravity_force = 1
        self._tick: float = update_tick if update_tick > 0 else 1 / 60
        self._paused = False
        self._clock = pyglet.clock.get_default()
        self._custom_callbacks = []

    def add_custom_callback(self, callback: Callable, *args):
        if callback and callback not in self._custom_callbacks:
            self._custom_callbacks.append((callback, args))
        else: raise ValueError("callback is undefined or already in the list")

    def remove_custom_callback(self, callback: Callable):
        for i in range(len(self._custom_callbacks)):
            if self._custom_callbacks[i][0] == callback:
                self._custom_callbacks.pop(i)
                return
        else: raise ValueError("callback not in the list")

    @property
    def custom_callbacks(self): return self._custom_callbacks

    def start(self):
        self._clock.schedule_interval(self.update, interval=self._tick)

    def update(self, dt):
        for callback, args in self._custom_callbacks:
            if args:
                callback(args)
            else: callback()



    def pause(self):
        ##some epic pause actions
        self._clock.unschedule(self.update)
        self._paused = True

    def resume(self):
        ##some epic resume actions
        self._clock.schedule_interval(self.update, self._tick)
        self._paused = False

    def stop(self):
        self._clock.unschedule(self.update)

    def schedule_once(self, callback: Callable, time: int, *args, **kwargs):
        self._clock.schedule_once(callback, time, args, kwargs)

    def schedule_interval(self, callback: Callable, interval: int, *args, **kwargs):
        self._clock.schedule_interval(callback, interval, args, kwargs)
