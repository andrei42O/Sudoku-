from engine import sudokuService

class Testing:
    def __init__(self):
        pass

    def run(self):
        self.__testEngine()
        print("Tests passed!")

    def __testEngine(self):
        serv = sudokuService()
        serv.setNumber(0, 0, 9)
        try:
            serv.setNumber(0, 1, 9)
        except Exception as e:
            assert(str(e) == "Wrong choice!")
        assert(serv.getElement(0, 1) == 9)
        serv.undo()
        assert(serv.getElement(0, 1) == -1)
        serv.undo()
        assert(serv.getElement(0, 0) == -1)
        try:
            serv.undo()
        except Exception as e:
            assert(str(e) == "There are no more actions to be undone!\n")

    