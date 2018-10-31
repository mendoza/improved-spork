import sys
from PyQt4 import QtCore, QtGui, uic

class Ui_MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        uic.loadUi("main.ui", self)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    windo = Ui_MainWindow()
    windo.show()
    sys.exit(app.exec_())
