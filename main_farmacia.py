# -*- coding: utf-8 -*-
from functools import partial
from PyQt4 import QtCore, QtGui, uic
import redis
import sys

reload(sys)
sys.setdefaultencoding("utf8")


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
        elif lista == "productos":
            farmid = self.listarprodfarm_cb.currentText()
            length = self.db.llen(lista)
            productos = []
            exclusivos = []
            for i in range(length):
                productos.append(self.db.lindex(lista, i))
            for prod in productos:
                if farmid in prod:
                    exclusivos.append(prod)
            #terminar despues de sanchez :v
            print(prod)

    def get_desempleados(self, lista):
        self.contrafarm_list.clear()
        if lista == "personas":
            length = self.db.llen(lista)
            '''print("personas: "),
            print(length)'''
            desempleados = []
            for i in range(length):
                indice = self.db.lindex(lista, i)
                personas = self.db.hmget(indice, "identidad")[0]
                if self.db.hmget(indice, "trabaja")[0] != "True":
                    self.contrafarm_list.addItem(personas)
                    print(self.db.hmget(personas, "nombre"))

    def set_farmaceuticos(self):
        self.contrafarm_cb.clear()
        "agarrar las farmacias que han sido creadas por dicho dueno"
        length = self.db.llen("farmacias")
        lista = []
        for i in range(length):
            index = self.db.lindex("farmacias", i)
            duenos = self.db.hmget(index, "duenos")[0].replace("[", "")
            duenos = duenos.replace("]", "")
            duenos = duenos.replace("'", "")
            duenos = duenos.split(",")
            if self.ident in duenos:
                lista.append(index)
        self.contrafarm_cb.addItems(lista)

    def contratar(self):

        if self.contrafarm_list.currentItem() != None:
            persona = self.contrafarm_list.currentItem().text()
            self.db.hset(persona, "trabaja", "True")
            farmacia = str(self.contrafarm_cb.currentText())
            hash_farm = self.db.hgetall(farmacia)
            lista = hash_farm["farmaceuticos"]
            lista = lista.replace("[", "")
            lista = lista.replace("]", "")
            lista = lista.replace("'", "")
            lista = lista.replace(" ", "")
            lista = lista.split(",")
            lista.append(str(persona))
            self.db.hset(farmacia, "farmaceuticos", lista)
            msg = QtGui.QMessageBox()
            msg.setIcon(QtGui.QMessageBox.Information)
            msg.setText("Contratado sin error")
            msg.setWindowTitle("ALERT")
            msg.setStandardButtons(QtGui.QMessageBox.Ok)
            msg.exec_()
        else:
            msg = QtGui.QMessageBox()
            msg.setIcon(QtGui.QMessageBox.Information)
            msg.setText("Error")
            msg.setWindowTitle("ALERT")
            msg.setStandardButtons(QtGui.QMessageBox.Ok)
            msg.exec_()

    def get_sociosfarma(self):
        self.anadirsocio_list.clear()
        farmacia = self.addsociofarm_cb.currentText()
        lista = self.db.hget(farmacia, "farmaceuticos")
        lista = lista.replace("[", "")
        lista = lista.replace("]", "")
        lista = lista.replace("'", "")
        lista = lista.replace(" ", "")
        lista = lista.split(",")
        print(len(lista))
        for i in range(len(lista)):
            if (self.db.hmget(lista[i],"departamento")[0] == "Socio" or lista[i] == " "):
                print("ya")
            else:
                self.anadirsocio_list.addItem(lista[i])
        

    def add_socios(self):
        if self.anadirsocio_list.currentItem() != None:
            persona=self.anadirsocio_list.currentItem().text()
            self.db.hset(persona, "departamento", "Socio")
            farmacia = str(self.addsociofarm_cb.currentText())
            hash_farm = self.db.hgetall(farmacia)
            lista = hash_farm["duenos"]
            lista = lista.replace("[", "")
            lista = lista.replace("]", "")
            lista = lista.replace("'", "")
            lista = lista.replace(" ", "")
            lista = lista.split(",")
            lista.append(str(persona))
            self.db.hset(farmacia,"duenos",lista)

            print("se ha guardado socio")
            msg = QtGui.QMessageBox()
            msg.setIcon(QtGui.QMessageBox.Information)
            msg.setText("Nuevo Socio")
            msg.setWindowTitle("ALERT")
            msg.setStandardButtons(QtGui.QMessageBox.Ok)
            msg.exec_()

    def get_sociosBorrar(self):
        self.borrarsocio_list.clear()
        farmacia = self.borrarsocio_cb.currentText()
        lista = self.db.hget(farmacia, "duenos")
        lista = lista.replace("[", "")
        lista = lista.replace("]", "")
        lista = lista.replace("'", "")
        lista = lista.replace(" ", "")
        lista = lista.split(",")
        for i in range(len(lista)):
            print(lista[i]),
            if  lista[i] == self.ident :
                print("es el mero")
            else:
                self.borrarsocio_list.addItem(lista[i])
        
        
    def borrar_socios(self):
        farmacia = self.borrarsocio_cb.currentText()
        persona=self.borrarsocio_list.currentItem().text()
        lista = self.db.hget(farmacia, "duenos")
        lista = lista.replace("[", "")
        lista = lista.replace("]", "")
        lista = lista.replace("'", "")
        lista = lista.replace(" ", "")
        lista = lista.split(",")
        for i in range(len(lista)):
            if persona == lista[i]:
                self.db.hset(persona, "departamento", "farmacia")
                del lista[i]
        self.db.hset(farmacia, "duenos", lista)

    def get_socios(self):
        self.listarsocio_list.clear()
        farmacia = self.listarsociofarm_cb.currentText()
        lista = self.db.hget(farmacia, "duenos")
        lista = lista.replace("[", "")
        lista = lista.replace("]", "")
        lista = lista.replace("'", "")
        lista = lista.replace(" ", "")
        lista = lista.split(",")
        
        self.listarsocio_list.addItems(lista)
                    
    def despedir(self):
        elegido = self.despidirfarm_list.currentItem().text()
        farmacia = self.despedirfarma_cb.currentText()
        lista = self.db.hget(farmacia, "farmaceuticos")
        lista = lista.replace("[", "")
        lista = lista.replace("]", "")
        lista = lista.replace("'", "")
        lista = lista.replace(" ", "")
        lista = lista.split(",")
        for i in range(len(lista)):
            if elegido == lista[i]:
                self.db.hset(elegido, "trabaja", "False")
                del lista[i]
        self.db.hset(farmacia, "farmaceuticos", lista)

    def borrar_farmacias(self):
        text = str(self.eliminarfarm_cb.currentText())
        length = self.db.llen("farmacias")
        farmacia = self.db.hgetall(text)
        lista = []
        for i in range(length):
            lista.append(self.db.lindex("farmacias", i))
        lista.remove(text)
        self.db.delete("farmacias")
        for index in lista:
            self.db.lpush("farmacias", index)
        self.db.delete(text)
        self.get_farmacias_lista()
        self.get_table("farmacias")

    def despedir_get(self):
        print("entre")
        self.despidirfarm_list.clear()
        farmacia = self.listafarmaceuticos_cb.currentText()
        lista = self.db.hget(farmacia, "farmaceuticos")
        lista = lista.replace("[", "")
        lista = lista.replace("]", "")
        lista = lista.replace("'", "")
        lista = lista.replace(" ", "")
        lista = lista.split(",")
        self.despidirfarm_list.addItems(lista)

    def despedir_get_list(self):
        self.listafarma_list.clear()
        farmacia = self.despedirfarma_cb.currentText()
        lista = self.db.hget(farmacia, "farmaceuticos")
        lista = lista.replace("[", "")
        lista = lista.replace("]", "")
        lista = lista.replace("'", "")
        lista = lista.replace(" ", "")
        lista = lista.split(",")
        self.listafarma_list.addItems(lista)

    def enviarbod(self):
        elegido = str(self.farmabodega_list.currentItem().text()
                      ).replace(" ", "")
        print(str(elegido) == "per_0000000000002")
        choosen = self.db.hgetall(elegido)
        choosen["departamento"] = "bodega"
        self.db.hmset(elegido, choosen)

    def get_farmacias_lista(self):
        self.eliminarfarm_cb.clear()
        self.listarprofarm_cb.clear()
        self.contrafarm_cb.clear()
        self.listafarmaceuticos_cb.clear()
        self.enviarfarma_cb.clear()
        self.pedirprofarm_cb.clear()
        self.addsociofarm_cb.clear()
        self.borrarsocio_cb.clear()
        self.eliminarprofarm_cb.clear()
        self.despedirfarma_cb.clear()
        self.listarsociofarm_cb.clear()
        
        "agarrar las farmacias que han sido creadas por dicho dueno"
        length = self.db.llen("farmacias")
        lista = []
        for i in range(length):
            index = self.db.lindex("farmacias", i)
            duenos = self.db.hmget(index, "duenos")[0].replace("[", "")
            duenos = duenos.replace("]", "")
            duenos = duenos.replace("'", "")
            duenos = duenos.split(",")
            if self.ident in duenos:
                lista.append(index)
        self.eliminarfarm_cb.addItems(lista)
        self.listarprofarm_cb.addItems(lista)
        self.contrafarm_cb.addItems(lista)
        self.listafarmaceuticos_cb.addItems(lista)
        self.enviarfarma_cb.addItems(lista)
        self.pedirprofarm_cb.addItems(lista)
        self.addsociofarm_cb.addItems(lista)
        self.borrarsocio_cb.addItems(lista)
        self.eliminarprofarm_cb.addItems(lista)
        self.despedirfarma_cb.addItems(lista)
        self.listarsociofarm_cb.addItems(lista)

    def get_empleados(self):
        self.farmabodega_list.clear()
        farmacia = self.enviarfarma_cb.currentText()
        lista = self.db.hget(farmacia, "farmaceuticos")
        lista = lista.replace("[", "")
        lista = lista.replace("]", "")
        lista = lista.replace("'", "")
        lista = lista.split(",")
        self.farmabodega_list.addItems(lista)

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
        self.contratarfarma_bt.clicked.connect(partial(self.contratar))
        self.contratarfarma_bt.clicked.connect(
            partial(self.get_desempleados, "personas")
        )

        self.empleados_bt.clicked.connect(partial(self.despedir_get))
        self.borrarfarma_bt.clicked.connect(partial(self.despedir))
        self.obtenerempleados_bt.clicked.connect(
            partial(self.despedir_get_list))

        self.enviarbod_bt.clicked.connect(partial(self.enviarbod))
        self.obtenerenv_bt.clicked.connect(partial(self.get_empleados))

        self.cargarsocio_bt.clicked.connect(partial(self.get_sociosfarma))
        self.cargarlistsocio_bt.clicked.connect(partial(self.get_socios))
        self.addsocio_bt.clicked.connect(partial(self.add_socios))
        self.addsocio_bt.clicked.connect(partial(self.get_sociosfarma))
        
        self.listaborrar_bt.clicked.connect(partial(self.get_sociosBorrar))
        self.borrarsocio_bt.clicked.connect(partial(self.borrar_socios))
        self.borrarsocio_bt.clicked.connect(partial(self.get_sociosBorrar))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindowFarmacia(0)
    window.show()
    sys.exit(app.exec_())
