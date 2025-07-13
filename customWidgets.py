from pyglet.gui import Slider


class CustomSlider(Slider):
    

    def __init__(self, min_val, max_val, x, y, *args, **kwargs):
        self.__processed_value = min_val
        self._minVal = min_val
        self._maxVal = max_val
        self.__diff = max_val - min_val
        self.__custom_handlers = []
        super().__init__(x, y, *args, **kwargs)


    def on_change(self, widget, value):
        self.__processed_value = self._minVal + self.__diff * value / 100
        for handler in self.__custom_handlers:
            handler(widget, value)
        super().on_change(widget, value)


    def set_processed_value(self, val):
        if self._minVal <= val <= self._maxVal:
            self.__processed_value = val
            self.value = (self.__processed_value - self._minVal) * 100 / self.__diff
        else: raise ValueError(f"new value is out of bounds: ({self._minVal} to {self._maxVal} (both including))")

    @property
    def processed_value(self): return self.__processed_value


    def add_event_handler(self, handler):
        if handler:
            if handler not in self.__custom_handlers:
                self.__custom_handlers.append(handler)

    def remove_event_handler(self, handler):
        if handler:
            if handler in self.__custom_handlers and (handler is not self.on_change):
                self.__custom_handlers.remove(handler)
