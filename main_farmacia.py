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
        "Guardar farmacias en DB"
        self.farmacia["nombre"] = self.nomfarm_edit.text()
        self.farmacia["id"] = "farm_" + str(self.db.get("contador_idfarmacia")).zfill(
            13
        )
        conta = int(float(self.db.get("contador_idfarmacia"))) + 1
        self.db.set("contador_idfarmacia", conta)
        self.farmacia["duenos"].append(self.ident)
        self.farmacia["productos"].append("")
        self.farmacia["direccion"] = self.ubifarm_edit.text()

        self.db.hmset(str(self.farmacia["id"]), self.farmacia)
        self.db.lpush("farmacias", self.farmacia["id"])
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText("Se ha creado una farmacia")
        msg.setWindowTitle("ALERT")
        msg.setStandardButtons(QtGui.QMessageBox.Ok)
        msg.exec_()
        self.get_farmacias_lista()
        self.get_table("farmacias")
        return

    def get_table(self, lista):
        "llena tabla de farmacias"
        if lista == "farmacias":
            self.verfarm_tb.setRowCount(0)
            self.verfarm_tb.setColumnCount(0)
            length = self.db.llen(lista)
            print(length)
            farmacias = []
            for i in range(length):
                index = self.db.lindex(lista, i)
                duenos = self.db.hmget(index, "duenos")[0].replace("[", "")
                duenos = duenos.replace("]", "")
                duenos = duenos.replace("'", "")
                duenos = duenos.split(",")
                print(duenos)
                if self.ident in duenos:
                    farmacias.append(index)
                self.verfarm_tb.setRowCount(len(farmacias))

            for i in range(len(farmacias)):
                farm = self.db.hgetall(farmacias[i])
                del farm["duenos"]
                del farm["productos"]
                del farm["farmaceuticos"]
                keys = farm.keys()
                self.verfarm_tb.setColumnCount(len(keys))
                self.verfarm_tb.setHorizontalHeaderLabels(keys)
                print(farm)
                for j in range(len(keys)):
                    self.verfarm_tb.setItem(
                        i, j, QtGui.QTableWidgetItem(str(farm[keys[j]]))
                    )

    def get_desempleados(self, lista):
        if lista == "personas":
            length = self.db.llen(lista)
            print("personas: "),
            print(length)
            desempleados = []
            for i in range(length):
                indice = self.db.lindex(lista, i)
                personas = self.db.hmget(indice, "identidad")[0]
                if self.db.hmget(indice, "trabaja")[0] != "True":
                    self.contrafarm_list.addItem(personas)
                    print(self.db.hmget(personas, "nombre"))

    def borrar_farmacias(self):
        text = str(self.eliminarfarm_cb.currentText())
        length = self.db.llen("farmacias")
        farmacia = self.db.hgetall(text)
        lista = []
        for i in range(length):
            lista.append(self.db.lindex("farmacias", i))
        lista.remove(text)
        self.db.delete("farmacias")
        # hacer for para que ilia ponga su rolita >:v
        for index in lista:
            self.db.lpush("farmacias", index)
        self.db.delete(text)
        self.get_farmacias_lista()
        self.get_table("farmacias")

    def get_farmacias_lista(self):
        self.eliminarfarm_cb.clear()
        "agarrar las farmacias que han sido creadas por dicho dueno"
        length = self.db.llen("farmacias")
        lista = []
        for i in range(length):
            index = self.db.lindex("farmacias", i)
            print("index" + str(index))
            duenos = self.db.hmget(index, "duenos")[0].replace("[", "")
            duenos = duenos.replace("]", "")
            duenos = duenos.replace("'", "")
            duenos = duenos.split(",")
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
        self.get_table("farmacias")
        self.get_desempleados("personas")
        self.crearfarm_bt.clicked.connect(partial(self.farmacias))
        self.borrarfarm_bt.clicked.connect(partial(self.borrar_farmacias))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindowFarmacia(0)
    window.show()
    sys.exit(app.exec_())
