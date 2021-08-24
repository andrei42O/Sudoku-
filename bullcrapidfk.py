import sys
import random
from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QBrush, QColor, QWindow

class test(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.tempLayout = QtWidgets.QHBoxLayout(self)
        self.btn = QtWidgets.QPushButton("press me!")
        self.btn.mousePressEvent = self.addW
        self.tempLayout.addWidget(self.btn)
        self.layout = self.tempLayout

    @QtCore.Slot()
    def addW(self, event):
        self.tempLayout.addWidget(QtWidgets.QPushButton("na ca mere"))
        self.update()


app = QtWidgets.QApplication([])
el = test()
el.show()
sys.exit(app.exec())
'''

def generateRow(self):
        row = QtWidgets.QWidget()
        tempLayout = QtWidgets.QHBoxLayout()
        #tempLayout.setSpacing(1)
        row.setLayout(tempLayout)
        for i in range(0, 3):
            self.__cells.append(cellGUI(self.__x, self.__y, int(self.__serv.getElement(self.__x, self.__y)), self.__serv))
            tempLayout.addWidget(self.__cells[-1])
            self.__y += 1
            #self.__nextCoordinates()
        #tempLayout.setSpacing(1)
        #tempLayout.setContentsMargins(0.25, 0.5, 0.25, 0.5)
        tempLayout.setSpacing(0)
        tempLayout.setContentsMargins(0, 0, 0, 0)
        return row

    def generateBox(self):
        box = QtWidgets.QWidget()
        tempLayout = QtWidgets.QGridLayout()
        box.setLayout(tempLayout)
        for i in range(0, 3):
            self.__x += 1
            self.__y = 3 * (self.__x // 3)
            tempLayout.addWidget(self.generateRow())
        #tempLayout.setSpacing(3)
        #tempLayout.setContentsMargins(0.25, 0.25, 0.25, 0.25)
        tempLayout.setSpacing(0)
        tempLayout.setContentsMargins(0, 0, 0, 0)
        box.setStyleSheet("border: 2px solid #6C757D")
        return box

    def generateRowGrid(self):
        rowGrid = QtWidgets.QWidget()
        tempLayout = QtWidgets.QHBoxLayout()
        rowGrid.setLayout(tempLayout)
        #tempLayout.setContentsMargins(0.5, 0.5, 0.5, 0.5)
        tempLayout.setSpacing(2)
        tempLayout.setContentsMargins(0, 0, 0, 0)
        for i in range (0, 3):
            tempLayout.addWidget(self.generateBox())
        return rowGrid

    def generateTableGUI(self):
        sudokuTable = QtWidgets.QWidget()
        tempLayout = QtWidgets.QGridLayout()
        sudokuTable.setLayout(tempLayout)
        tempLayout.setSpacing(2)
        tempLayout.setContentsMargins(3, 3, 3, 3)
        for i in range(0, 3):
            tempLayout.addWidget(self.generateRowGrid())
        sudokuTable.setStyleSheet("background-color: #343A40; padding: 5px 5px 5px 5px;")
        return sudokuTable
'''