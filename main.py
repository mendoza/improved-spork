import sys
import redis
from PyQt4 import QtCore, QtGui, uic

class Ui_MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent=parent)
        #QtGui.QMainWindow.__init__(self)
        # uic.loadUi("main.ui", self)
	db = redis.StrictRedis(host="159.89.34.186",password="papitopiernaslargas69",db=0,port="6379")
	self.label.setText(db.get("CasoClave"))
        super(Ui_MainWindow, self).__init__()
        self.setupUI(self)

    def initUI(self):

        self.resize(640, 480)
        self.setWindowTitle('Probando')
        self.center()

        self.show()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())
 