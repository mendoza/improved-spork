# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import redis
from PyQt4 import QtCore, QtGui, uic


class MainWindowFarmacia(QtGui.QMainWindow):
    def farmacia(self):
        length = self.db.llen("farmacias")
        lista = []

        for i in range(length)
            lista.append(self.db.lindex("farmacias",i))
        self.farmacia["nombre"]=self.nomfarm_edit.text()
        self.farmacia["id"]=self.db.get(contador_idfarmacia)
        self.farmacia["nombre"]=self.nomfarm_edit.text()


    def __init__(self):
        self.farmacia={
		    "nombre":"",
		    "id": registro.id_edit ,
		    "duenos": [],
		    "productos": [],
		    "direccion": "",
		    "farmaceuticos": []
	}
        super(MainWindowFarmacia, self).__init__()
        QtGui.QMainWindow.__init__(self)
        uic.loadUi("./ui/Farmacia.ui", self)
        self.db = redis.StrictRedis(
            host="159.89.34.186", password="papitopiernaslargas69", db=0, port="6379"
        )
        print("vamos a la playa")


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindowFarmacia()
    window.show()
    sys.exit(app.exec_())