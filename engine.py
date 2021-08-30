from observer import ButtonPressObserver, FocusObservable, Observable

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


class sudokuService(Observable, FocusObservable):
    def __loadMatrix(self):
        matrix = []
        with open("sol.txt", "r") as f:
            for i in range(0, 8):
                line = f.readline()
                el = str(line).split(' ')
                el.pop()
                for nr in el:
                    matrix.append(int(nr))
                print(line)
        for i in range(0, 9):
            matrix.append(-1)
        print(matrix)
        return matrix

    def __init__(self):
        super().__init__()
        self.__baseMatrix = self.__loadMatrix()
        self.__matrix = self.__baseMatrix[:]
        self.__undo = undoClass()
        self.__x = None
        self.__y = None
        self.__currentCell = None
        self.__filledCells = 72
        self.__startingFilledCells = 72

    def __resetCellCoordinates(self):
        self.__x, self.__y, self.__currentCell = None, None, None

    def __checkLine(self, x, y):
        for i in range(0, 9):
            if i != y and self.__matrix[x * 9 + i] == self.__matrix[x * 9 + y]:
                return False
        return True

    def __checkColumn(self, x, y):
        for i in range(0, 9):
            el1 = self.__matrix[i * 9 + y]
            el2 = self.__matrix[x * 9 + y]
            print(el1, el2, abs(el2 - el1) < 0.001)
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
            if self.__matrix[x * 9 + y] == -1:
                pass
            else:
                self.__undo.addAction(self.setNumber, x, y, self.__matrix[x * 9 + y], "undo")
                if self.__currentCell != None:
                    print(self.__currentCell.getX(), self.__currentCell.getY())
                else:
                    raise Exception("Please select a cell first!")
        #We deleted the contect of the current cell and unfocused it, so the currentCell doesn't exist
        self.__matrix[x * 9 + y] = oldNumber
        if str(T).lower() == "undo":
            self.__resetCellCoordinates()
        Observable.notify(self, x, y)
        if self.__currentCell != None:
            self.__currentCell.focusCell(None)

    def setNumber(self, x, y, number, T = None):
        if str(T).lower() != "undo":
            self.__undo.addAction(self.deleteNumber, x, y, self.__matrix[x * 9 + y], "undo")
        self.__matrix[x * 9 + y] = number
        Observable.notify(self, x, y) # set the number in the cell and draw it without focus
        if str(T).lower() != "undo" and self.__currentCell != None:
            self.__currentCell.focusCell(None) # focus the cell
        if str(T).lower() == "undo":
            self.__resetCellCoordinates()
        self.__checkChoice(x, y)
        self.__filledCells += 1
        #game WON
        print("We have currently {} cells left".format(81 - self.__filledCells))
        if self.__filledCells == 81: 
            print("Congrats you won!")
            raise Exception("Congratulations! You Won!")
            #to fill with close and new game box
            pass
        
    def getElement(self, x, y):
        return self.__matrix[x * 9 + y]
    
    def undo(self):
        self.__undo.undoAction()
        
    def getMatrix(self):
        return self.__matrix[:]

    def reset(self):
        self.__matrix = self.__baseMatrix[:]
        self.__undo.reset()
        self.__filledCells = self.__startingFilledCells
        self.__resetCellCoordinates()

    def setCurrentCell(self, cell):
        if self.__x != None and self.__y != None and self.__currentCell != cell:
            FocusObservable.unfocusObject(self)
        self.__x = cell.getX()
        self.__y = cell.getY()
        self.__currentCell = cell
        FocusObservable.setFocusedObj(self, cell)

    def recieveNumber(self, nr):
        if self.__x != None and self.__y != None:
            self.setNumber(self.__x, self.__y, int(nr))
            print("Recieved!")

    def emptyCell(self):
#        print(self.__x, self.__y)
        if self.__x != None and self.__y != None:
            self.deleteNumber(self.__x, self.__y, -1)
        else:
            raise Exception("There is not cell selected!")
