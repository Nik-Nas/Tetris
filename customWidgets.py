from inspect import signature
from pyglet.gui import Slider


class CustomSlider(Slider):
    

    def __init__(self, minVal, maxVal, x, y, *args, **kwargs):
        self._processed_value = minVal
        self._minVal = minVal
        self._maxVal = maxVal
        self.__diff = maxVal - minVal
        self.__custom_handlers = []
        super().__init__(x, y, *args, **kwargs)


    def on_change(self, widget, value):
        self._processed_value = self._minVal + self.__diff * value / 100
        for handler in self.__custom_handlers:
            handler(widget, value)
        super().on_change(widget, value)


    def set_processed_value(self, val):
        if self._minVal <= val <= self._maxVal:
            self._processed_value = val
            self.value = (self._processed_value - self._minVal) * 100 / self.__diff
        else: raise ValueError(f"new value is out of bounds: ({minVal} to {maxVal} (both including))")


    def add_event_handler(self, handler):
        if handler:
            #print(signature(handler).parameters)
            if handler not in self.__custom_handlers:
                self.__custom_handlers.append(handler)

    def remove_event_handler(self, handler):
        if handler:
            if handler in self.__custom_handlers and (handler is not self.on_change):
                self.__custom_handlers.remove(handler)
##
##
