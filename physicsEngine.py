import pyglet.clock


class PhysicsEngine:

    def __init__(self, update_tick, gravity=None):
        if gravity is not None: self.__gravity_force = gravity.length
        else: self.__gravity_force = 1
        self._tick = update_tick if update_tick > 0 else 1/60
        self._paused = False
        self._clock = pyglet.clock.get_default()
        self.__custom_callbacks = []
        self.__fallable = []


    def add_custom_callback(self, callback):
        if callback:
            self.__custom_callbacks.append(callback)


    def remove_custom_callback(self, callback):
        if callback:
            self.__custom_callbacks.remove(callback)


    def start(self):
        self._clock.schedule_interval(self.update, interval=self._tick)
        self._clock.tick()
        self._clock.update_time()


    def update(self, dt):
        for callback in self.__custom_callbacks:
            callback()
        pass

    def pause(self):
        ##some epic pause actions
        self._clock.unschedule(self.update)
        self._paused = True


    def resume(self):
        ##some epic resume actions
        self._clock.schedule_interval(self.update, self._tick)
        self._paused = False

    def stop(self):
        self._clock.schedule_interval(self.update, self._tick)
        
