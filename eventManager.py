class EventManager:
    
    def __init__(self):
        self.__events = {}

    def add_event_type(self, type_):
        if type_ and type_ not in self.__events:
            self.__events[type_] = []

    def add_event(self, type_, event):
        if not type_: raise ValueError("given type is empty")
        if not event: raise ValueError("given event is empty")
        if type_ not in self.__events: raise TypeError("given type of events does not exist")
        self.__events[type_].append(event)
            
