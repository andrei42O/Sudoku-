from observer import Observable

class undoClass:
    def __init__(self):
        self.__undo = []
    
    def undoAction(self):
        if not len(self.__undo):
            raise Exception("There are no more actions to be undone!\n")
        tempElem = self.__undo.pop(-1)
        tempElem["function"](*tempElem["arguments"])


    def addAction(self, funct, *args):
        self.__undo.append({"function": funct, "arguments": args})

    def reset(self):
        self.__undo.clear()


class sudokuService(Observable):
    def __init__(self):
        super().__init__()
        self.__baseMatrix = [-1] * 81
        self.__matrix = self.__baseMatrix[:]
        self.__undo = undoClass()
        self.__x = None
        self.__y = None

    def __checkLine(self, x, y):
        for i in range(0, 9):
            if i != y and self.__matrix[x * 9 + i] == self.__matrix[x * 9 + y]:
                return False
        return True

    def __checkColumn(self, x, y):
        for i in range(0, 9):
            if i != x and self.__matrix[i * 9 + y] == self.__matrix[x * 9 + y]:
                return False
        return True

    def __checkBox(self, x, y):
        startX = (x // 3) * 3
        startY = (y // 3) * 3
        for i in range(0, 3):
            for j in range(0, 3):
                if startX + i != x and startY + j != y and self.__matrix[(startX + i) * 9 + startY + j] == self.__matrix[x * 9 + y]:
                    return False
        return True

    def __checkChoice(self, x, y):
        try:
            x = int(x)
            y = int(y)
            if x < 0 or x > 8 or y < 0 or y > 8:
                raise Exception()
        except:
            raise Exception("Invalid Coordinates!")
        if not (self.__checkLine(x, y) and self.__checkColumn(x, y) and self.__checkBox(x, y)):
            raise Exception("Wrong choice!")

    def checkValidity(self, x, y):
        try:
            x = int(x)
            y = int(y)
            if x < 0 or x > 8 or y < 0 or y > 8:
                raise Exception()
        except:
            raise Exception("Invalid Coordinates!")
        if self.getElement(x, y) == -1:
            return True
        return bool(self.__checkLine(x, y) and self.__checkColumn(x, y) and self.__checkBox(x, y))

    def deleteNumber(self, x, y, oldNumber, T = None):
        if str(T).lower() != "undo":
            self.__undo.addAction(self.setNumber, x, y, self.__matrix[x * 9 + y], "undo")
        self.__matrix[x * 9 + y] = oldNumber
        Observable.notify(self, x, y)

        
    def setNumber(self, x, y, number, T = None):
        if str(T).lower() != "undo":
            self.__undo.addAction(self.deleteNumber, x, y, self.__matrix[x * 9 + y], "undo")
        self.__matrix[x * 9 + y] = number
        self.__checkChoice(x, y)
        Observable.notify(self, x, y)
        
    def getElement(self, x, y):
        return self.__matrix[x * 9 + y]
    
    def undo(self):
        self.__undo.undoAction()
        

    def getMatrix(self):
        return self.__matrix[:]

    def reset(self):
        self.__matrix = self.__baseMatrix[:]
        self.__undo.reset()

    def setCurrentCoordinates(self, x, y):
        if self.__x != None and self.__y != None:
            #notify the last cell to unfocus
            pass
        self.__x = x
        self.__y = y
