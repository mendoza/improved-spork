# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding("utf8")
import redis
from PyQt4 import QtCore, QtGui, uic
from functools import partial


class MainWindowFarmacia(QtGui.QMainWindow):
    def farmacias(self):
        length = self.db.llen("farmacias")
        lista = []
        for i in range(length):
            lista.append(self.db.lindex("farmacias", i))

        self.farmacia["nombre"] = self.nomfarm_edit.text()
        self.farmacia["id"] = "farm_"+str(self.db.get("contador_idfarmacia")).zfill(13)
        conta = int(float(self.db.get("contador_idfarmacia"))) + 1
        self.db.set("contador_idfarmacia", conta)
        self.farmacia["duenos"].append(self.ident)
        self.farmacia["productos"].append("")
        self.farmacia["direccion"] = self.ubifarm_edit.text()

        self.db.hmset(
            str(self.farmacia["id"]), self.farmacia)
        self.db.lpush("farmacias", self.farmacia["id"])
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText("Se ha creado una farmacia")
        msg.setWindowTitle("ALERT")
        msg.setStandardButtons(QtGui.QMessageBox.Ok)
        msg.exec_()

        return

    def get_farmacias_lista(self):
        length = self.db.llen("farmacias")
        lista = []
        for i in range(length):
            index =self.db.lindex("farmacias",i)
            duenos = self.db.hmget(index,"duenos")[0].replace('[','')
            duenos = duenos.replace(']','')
            duenos = duenos.replace('\'','')
            duenos = duenos.split(',')
            if self.ident in duenos:
                lista.append(index)
        self.eliminarfarm_cb.addItems(lista)
    def __init__(self, ident):
        self.farmacia = {
            "nombre": "",
            "id": "",
            "duenos": [],
            "productos": [],
            "direccion": "",
            "farmaceuticos": [],
        }
        super(MainWindowFarmacia, self).__init__()
        self.ident = ident
        QtGui.QMainWindow.__init__(self)
        uic.loadUi("./ui/Farmacia.ui", self)
        self.db = redis.StrictRedis(
            host="159.89.34.186", password="papitopiernaslargas69", db=0, port="6379"
        )
        self.get_farmacias_lista()
        self.crearfarm_bt.clicked.connect(partial(self.farmacias))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindowFarmacia(0)
    window.show()
    sys.exit(app.exec_())
