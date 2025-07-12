from gui import LinkedVar

class DataManager:
    def __init__(self):
        self.linkedVariables = {}


    def addLinked(self, name, val):
        if name in self.linkedVariables: raise ValueError("name", name, "already exists in list"):
        else self.linkedVariables[name] = LinkedVar(val)

    














        
