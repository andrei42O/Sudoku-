import sys
import random
from engine import sudokuService
from test import Testing
from PySide6 import QtCore, QtWidgets
from observer import ButtonPressObservable, FocusObserver, Observer

def errorBox(err):
    box = QtWidgets.QMessageBox()
    box.setText(err)
    box.setWindowTitle("Warning!")
    box.exec()

class cellGUI(QtWidgets.QLabel, Observer, FocusObserver):
    def __init__(self, x, y, nr, serv):
        super().__init__()
        self.__serv = serv
        self.__x = x
        self.__y = y
        self.__baseValue = self.__nr = nr
        self.__valid = 1
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.__drawCell()
        self.setMinimumSize(30, 30)
        self.mousePressEvent = self.focusCell
        self.setContentsMargins(0, 0, 0, 0)
        self.__serv.addObserver(self)
    
    def __drawCell(self):
        if self.__nr != -1:
            self.setText(str(self.__nr))
        else: 
            self.setText("")
        if self.__valid:
            self.setStyleSheet("color: black; background-color: #E9ECEF; border: 1px solid black;")
        else:
            self.setStyleSheet("color: red; background-color: #E9ECEF; border: 1px solid red;")


    @QtCore.Slot()
    def updateCell(self, event):
        if self.__nr == -1:
            self.__nr = 6
            try:
                self.__serv.setNumber(self.__x, self.__y, self.__nr)
            except Exception:
                self.__valid = 0
            self.__drawCell()

    @QtCore.Slot()
    def focusCell(self, event):
        if self.__nr != -1:
            self.setText(str(self.__nr))
        else: 
            self.setText("")
        if self.__valid:
            self.setStyleSheet("color: black; background-color: #E9ECEF; border: 3px solid black;")
        else:
            self.setStyleSheet("color: red; background-color: #E9ECEF; border: 3px solid red;")
        self.__serv.setCurrentCell(self)

    def reset(self):
        self.__nr = self.__baseValue
        self.__valid = 1
        self.__drawCell()

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    #inherited functions

    def update(self, x, y, type = None):
        #Inherited from 'Observer'
        if x == self.__x and y == self.__y:
            try:
                self.__nr = self.__serv.getElement(x, y)
                self.__valid = self.__serv.checkValidity(x, y)
                self.__drawCell()
            except Exception as e:
                errorBox(str(e))

    def focusUpdate(self):
        self.__drawCell()

class button(QtWidgets.QPushButton):
    def __init__(self, text, serv):
        super().__init__()
        self.__serv = serv
        self.setText(text)
        self.setStyleSheet("background-color: #4cc9f0; color: #e5e5e5;")
        self.setFixedSize(50, 50)
        self.setContentsMargins(0, 0, 0, 0)
        self.mousePressEvent = self.emitSignal
        #self.connect(btn, QtCore.SIGNAL("clicked()"), self.emitSignal(btn))
    
    @QtCore.Slot()
    def emitSignal(self, event):
        '''
            Emit a notification to change the cell content
        '''
        print(self.text())
        self.__serv.recieveNumber(int(self.text()))

class buttons(QtWidgets.QWidget):
    def __init__(self, serv):
        super().__init__()
        self.__serv = serv
        layout = QtWidgets.QVBoxLayout()
        #layout.addStretch()
        self.setLayout(layout)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        k = 1
        for i in range(0, 3):
            tempW = QtWidgets.QWidget()
            tempW.setStyleSheet("background-color: black;")
            tempW.setContentsMargins(0, 0, 0, 0)

            tempL = QtWidgets.QHBoxLayout()
            tempL.setSpacing(2)
            tempL.setContentsMargins(0, 0, 0, 0)

            tempW.setLayout(tempL)
            for j in range(0, 3):
                tempL.addWidget(button(str(k), self.__serv))
                k += 1
            layout.addWidget(tempW)
        layout.setAlignment(QtCore.Qt.AlignCenter) #without this line the buttons won't remaing close and  centered

class SudokuTable(QtWidgets.QWidget):

    def __nextCoordinates(self):
        self.__y += 1
        self.__x = self.__x + self.__y // 9
        self.__y %= 9

    def __generateCells(self):
        for i in range(0, 81):
            self.__cells.append(cellGUI(self.__x, self.__y, self.__serv.getElement(self.__x, self.__y), self.__serv))
            self.__nextCoordinates()

    def __generateBox(self, x, y):
        '''
            top left corner coordinates
            x - integer
            y - integer
        '''
        tempW = QtWidgets.QWidget()
        tempLayout = QtWidgets.QVBoxLayout()
        tempW.setLayout(tempLayout)
        tempLayout.setSpacing(1)
        for i in range(0, 3):
            tempL = QtWidgets.QHBoxLayout()
            #tempL.setContentsMargins(0, 0, 0, 0)
            tempL.setSpacing(1)
            for j in range(0, 3):
                tempL.addWidget(self.__cells[(x + i) * 9 + y + j])
            tempLayout.addLayout(tempL)
        tempW.setContentsMargins(0, 0, 0, 0)
        tempLayout.setContentsMargins(2, 2, 2, 2)
        return tempW
    
    def generateTableGUI(self):
        self.__generateCells()
        x = 0
        y = 0
        El = QtWidgets.QWidget()
        Layout = QtWidgets.QVBoxLayout()
        El.setContentsMargins(0, 0, 0, 0)
        Layout.setContentsMargins(2, 2, 2, 2)
        Layout.setSpacing(0)
        for i in range(0, 3):
            tempEl = QtWidgets.QWidget()
            tempL = QtWidgets.QHBoxLayout()
            tempEl.setLayout(tempL)
            tempL.setSpacing(0)
            tempEl.setContentsMargins(0, 0, 0, 0)
            tempL.setContentsMargins(0, 0, 0, 0)
            y = 0
            for j in range(0, 3):
                tempL.addWidget(self.__generateBox(x, y))
                y += 3
            x += 3
            Layout.addWidget(tempEl)
        El.setLayout(Layout)
        El.setStyleSheet("background-color: #343A40;")
        return El

    def __assignSignals(self):
        QtCore.QObject.connect(self.resetButton, QtCore.SIGNAL('clicked()'), self.resetTable)
        QtCore.QObject.connect(self.undoButton, QtCore.SIGNAL('clicked()'), self.undo)
        QtCore.QObject.connect(self.deleteButton, QtCore.SIGNAL('clicked()'), self.emptyCell)

    def __rightPart(self):
        mainL = QtWidgets.QVBoxLayout()
        tempL = QtWidgets.QHBoxLayout()
        tempL.addWidget(self.resetButton)
        tempL.addWidget(self.undoButton)
        templ2 = QtWidgets.QHBoxLayout()
        templ2.addWidget(self.deleteButton)
        mainL.addLayout(tempL)
        mainL.addLayout(templ2)
        mainL.addWidget(buttons(self.__serv))
      #  mainL.setAlignment(QtCore.Qt.AlignCenter)
        return mainL

    def __init__(self, serv):
        super().__init__()
        self.__serv = serv
        self.__x = 0
        self.__y = 0
        self.__cells = []
        self.tempLayout = QtWidgets.QHBoxLayout(self)
        self.setLayout(self.tempLayout)
        self.sudokuTable = self.generateTableGUI()
        self.tempLayout.addWidget(self.sudokuTable)
        self.resetButton = QtWidgets.QPushButton("RESET")
        self.undoButton = QtWidgets.QPushButton("UNDO")
        self.deleteButton = QtWidgets.QPushButton("DELETE")
        self.resetButton.setStyleSheet("background-color: #00bbf9;")
        self.undoButton.setStyleSheet("background-color: #00bbf9;")
        self.deleteButton.setStyleSheet("background-color: #00bbf9;")
        self.tempLayout.addLayout(self.__rightPart())
        self.__assignSignals()
        self.setWindowTitle("Sudoku!")
        

    @QtCore.Slot()
    def resetTable(self):
        self.__x, self.__y = 0, 0
        for cell in self.__cells:
            cell.reset()
        self.tempLayout.update()
        self.__serv.reset()

    @QtCore.Slot()
    def undo(self):
        try:
            self.__serv.undo()
        except Exception as e:
            errorBox(str(e))
    
    @QtCore.Slot()
    def emptyCell(self):
        try:
            self.__serv.emptyCell()
        except Exception as e:
            errorBox(str(e))
        
def generateRandomMatrix(h, l):
    matrix = []
    for i in range(0, h):
        for j in range(0, l):
            matrix.append(random.randint(0, 9))
    return matrix

def runTests():
    t = Testing()
    t.run()

if __name__ == "__main__":
   # runTests()
    app = QtWidgets.QApplication([])
    serv = sudokuService()
    widget = SudokuTable(serv)
    widget.show()

    sys.exit(app.exec())
