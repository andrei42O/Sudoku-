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

############################################

class FocusObserver:
    def __init__(self) -> None:
        pass

    def focusUpdate(self):
        pass

class FocusObservable:
    def __init__(self) -> None:
        self.__obj = None

    def setFocusedObj(self, ob):
        self.__obj = ob

    def unfocusObject(self):
        self.__obj.focusUpdate()

############################################

class ButtonPressObserver:
    def __init__(self) -> None:
        pass

    def recieveNumber(self, nr):
        pass

class ButtonPressObservable:
    def __init__(self):
        self.__objs = []

    def addButtonListeners(self, ob):
        self.__objs.append(ob)

    def notifyButtonPressed(self, nr):
        for ob in self.__objs:
            ob.recieveNumber(nr)