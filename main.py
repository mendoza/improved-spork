import sys
import redis
from PyQt4 import QtCore, QtGui, uic

<<<<<<< HEAD

class Ui_MainWindow(QtGui.QMainWindow):
=======
class MainWindow(QtGui.QMainWindow):
>>>>>>> 27b1c64b0a574eb9e7c28e9051a594d6e5a06944
    def __init__(self):
        super(MainWindow, self).__init__()
        QtGui.QMainWindow.__init__(self)
        uic.loadUi("main.ui", self)
<<<<<<< HEAD


=======
	db = redis.StrictRedis(host="159.89.34.186",password="papitopiernaslargas69",db=0,port="6379")
	self.label.setText(db.get("CasoClave"))
>>>>>>> 27b1c64b0a574eb9e7c28e9051a594d6e5a06944
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
 