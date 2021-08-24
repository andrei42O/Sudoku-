class Observer:
    def __init__(self):
        pass
    
    def undo(self, *args):
        pass

class Observable:
    def __init__(self):
        self.__objs = []

    def addObserver(self, ot):
        self.__objs.append(ot)

    def notify(self, x, y):
        for ob in self.__objs:
            ob.undo(x, y)