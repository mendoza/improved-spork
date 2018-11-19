import sys
reload(sys)
sys.setdefaultencoding('utf8')
import redis
from PyQt4 import QtCore, QtGui, uic

class MainWindowLab(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindowLab, self).__init__()
        QtGui.QMainWindow.__init__(self)
        uic.loadUi("./ui/Laboratorio.ui", self)
        self.db = redis.StrictRedis(
            host="159.89.34.186", password="papitopiernaslargas69", db=0, port="6379"
        )


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindowLab()
    window.show()
    sys.exit(app.exec_())
