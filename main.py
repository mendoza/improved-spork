import sys
import redis
from PyQt4 import QtCore, QtGui, uic


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        QtGui.QMainWindow.__init__(self)
        uic.loadUi("./ui/main.ui", self)
        db = redis.StrictRedis(
            host="159.89.34.186", password="papitopiernaslargas69", db=0, port="6379"
        )


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
