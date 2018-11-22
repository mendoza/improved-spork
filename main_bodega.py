# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding("utf8")
import redis
from PyQt4 import QtCore, QtGui, uic
from functools import partial

class MainWindowBodega(QtGui.QMainWindow):
    def llenartablaprod(self):
        farmacias = []
        for i in range(self.db.llen("farmacias")):
            index = self.db.lindex("farmacias",i)
            in_hash = self.db.hgetall(index)
            lista = in_hash["farmaceuticos"]
            lista = lista.replace("[","")
            lista = lista.replace("]","")
            lista = lista.replace("\'","") 
            #OCUPAMOS ALGUIEN DE BODEGA Y OCUPAS QUE HAGAN UN PEDIDO :v CREO NO ESTOY SEGURO PARA QUE HICE ESTO :v
            # DECILE A MATA QUE HICE TABLEWIDGET... QUE LE CAMBIE A ALGO AHI
            #BASICAMENTE ESTO CONSIGUE DONDE TRABAJA EL MAN Y LUEGO AGREGA LOS PRODUCTOS DE AHI :v
            #decime el nombre de la tabla para cambiar las variables probodega_tb
            #le puedo dar push, me estoy muriendoxdsda PERO CAMBIA LA HORA
            #no hemso terminado...
            #SOLO UN POCO MAS CHIOCOS, SI SE PUEDE -SANCHEZ
            #VAMOS PERROS
            #DEJEMOS QUE ESTOS SE VAYAN CON EL PUSH PARA RECORDAR ESTE MOMENTO JAJAJAJ
            #PERDIMOS A MATA, HOUSTON TENEMS PROBLEMAS
            #QUE PASO QUE 
            #Se habra dormido sobre el teclado?
            lista = lista.split(",")
            if self.ident in lista:
                farmacias.append(index)
        productos = []
        exclusivos = []
        for farmid in farmacias:
            farm_hash = self.db.hget(farmid,"productos")[0]
            farm_hash = farm_hash.replace("[","")
            farm_hash = farm_hash.replace("]","")
            farm_hash = farm_hash.replace("\'","")
            farm_hash = farm_hash.split(',')
            for prod in farm_hash:
                productos.append(prod)
        self.probodega_tb.setRowCount(len(productos))
        for i in range(len(productos)):
            farm = self.db.hgetall(productos[i])
            keys = farm.keys()
            self.probodega_tb.setColumnCount(len(keys))
            self.probodega_tb.setHorizontalHeaderLabels(keys)
            print(farm)
            for j in range(len(keys)):
                self.probodega_tb.setItem(
                    i, j, QtGui.QTableWidgetItem(str(farm[keys[j]])))

    def llenarprodborrar(self):
        self.borrar_cb.clear()
        farmacias = []
        for i in range(self.db.llen("farmacias")):
            index = self.db.lindex("farmacias",i)
            in_hash = self.db.hgetall(index)
            lista = in_hash["farmaceuticos"]
            lista = lista.replace("[","")
            lista = lista.replace("]","")
            lista = lista.replace("\'","") 
            lista = lista.split(",")
            if self.ident in lista:
                farmacias.append(index)
        productos = []
        exclusivos = []
        for farmid in farmacias:
            farm_hash = self.db.hget(farmid,"productos")[0]
            farm_hash = farm_hash.replace("[","")
            farm_hash = farm_hash.replace("]","")
            farm_hash = farm_hash.replace("\'","")
            farm_hash = farm_hash.split(',')
            for prod in farm_hash:
                productos.append(prod)
        self.borrar_cb.addItems(productos)
    def borrarprod(self):
        #-----------lista-----------------
        elegido = self.borrar_cb.currentText()
        productos = []
        for i in range(self.db.llen("productos")):
            productos.append(self.db.lindex("productos",i))
        if elegido in productos:
            productos.remove(elegido)
            self.db.set("productos",productos)
        #-----------farma------------------
        farmacias = []
        for i in range(self.db.llen("farmacias")):
            index = self.db.lindex("farmacias",i)
            in_hash = self.db.hgetall(index)
            lista = in_hash["farmaceuticos"]
            lista = lista.replace("[","")
            lista = lista.replace("]","")
            lista = lista.replace("\'","") 
            lista = lista.split(",")
            if self.ident in lista:
                farmacias.append(index)
        for farmid in farmacias: 
            farm_hash = self.db.hget(farmid,"productos")[0]
            farm_hash = farm_hash.replace("[","")
            farm_hash = farm_hash.replace("]","")
            farm_hash = farm_hash.replace("\'","")
            farm_hash = farm_hash.split(',')
            if elegido in farm_hash:
                farm_hash.remove(elegido)
                self.db.hset(farmid,"productos",farm_hash)
    def __init__(self, ident):
        super(MainWindowBodega, self).__init__()
        QtGui.QMainWindow.__init__(self)
        uic.loadUi("./ui/Bodega.ui", self)
        self.ident = ident
        self.db = redis.StrictRedis(
            host="159.89.34.186", password="papitopiernaslargas69", db=0, port="6379"
        )
        self.llenartablaprod()
        self.eliminar_bt_2.clicked.connect(partial(self.borrarprod))

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindowBodega(0)
    window.show()
    sys.exit(app.exec_())
