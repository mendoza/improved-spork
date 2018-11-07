import sys
import redis
from PyQt4 import QtCore, QtGui, uic

class Ui_MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        uic.loadUi("main.ui", self)
	db = redis.StrictRedis(host="159.89.34.186",password="papitopiernaslargas69",db=0,port="6379")
	self.label.setText(db.get("saludo"))
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())
 