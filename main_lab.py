import sys

reload(sys)
sys.setdefaultencoding("utf8")
import redis
from PyQt4 import QtCore, QtGui, uic
from functools import partial


class MainWindowLab(QtGui.QMainWindow):
    def CrearP(self):
        self.producto["id"] = "prod_" + str(self.db.get("contador_idproducto")).zfill(
            13
        )
        conta = int(float(self.db.get("contador_idproducto"))) + 1
        self.db.set("contador_idproducto", conta)
        self.producto["nombre"] = str(self.NombreP_edit.text())
        self.producto["fabricante"] = str(self.Fabricante_cb.currentText())
        self.producto["costoVenta"] = int(self.CostoVenta_sb.value())
        self.producto["coste"] = int(self.Coste_sb.value())
        self.producto["unidad"] = int(self.Unidades_sb.value())
        SeguridadP = False
        if bool(self.Seguridad_cb.isTristate()):
            SeguridadP = True
        self.producto["seguridad"] = bool(SeguridadP)
        self.producto["familia"] = str(self.Familia_cb.currentText())
        self.db.lpush("productos",self.producto["id"])
        self.db.hmset(self.producto["id"],self.producto)
        length = self.db.llen("productos")
        print(length)
        productosL = []
        for i in range(length):
            index = self.db.lindex("productos",i)
            if self.db.hget(self.db.hget(index,"fabricante"),"jefe")==self.ident:
                productosL.append(index)
        self.db.hset(str(self.Fabricante_cb.currentText()),"productos",productosL)
        self.getProducto("productos")
        
    def CrearLab(self):
        self.laboratorio["id"] = "lab_" + str(self.db.get("contador_idLab")).zfill(13)
        conta = int(float(self.db.get("contador_idLab"))) + 1
        self.db.set("contador_idLab", conta)
        self.laboratorio["nombre"] = str(self.NombreL_edit.text())
        self.laboratorio["direccion"] = str(self.DireccionL_edit.text())
        self.laboratorio["jefe"] = self.ident
        self.db.lpush("laboratorios",self.laboratorio["id"])
        self.db.hmset(self.laboratorio["id"],self.laboratorio)
        self.getFaricante()
        self.ListarLabs()
            
    def CrearFamilia(self):
        famP = str(self.Familia_edit.text())
        self.db.lpush("familias",famP)
        self.getListFamilias()
        

    def getListFamilias(self):
        self.Familia_cb.clear()
        self.familia_list.clear()
        length = self.db.llen("familias")
        lista = []
        for i in range(length):
            index = self.db.lindex("familias", i)
            lista.append(index)
        self.Familia_cb.addItems(lista)
        self.familia_list.addItems(lista)

    def getFaricante(self):
        self.Fabricante_cb.clear()
        length = self.db.llen("laboratorios")
        lista2 = []
        for i in range(length):
            index = self.db.lindex("laboratorios",i)
            lista2.append(index)
        self.Fabricante_cb.addItems(lista2)

    def ListarLabs(self):
        self.Fabricante_cb.clear()
        self.LabsE_list.clear()
        length = self.db.llen("laboratorios")
        lista = []
        for i in range(length):
            index = self.db.lindex("laboratorios", i)
            duenos = self.db.hmget(index, "jefe")[0]
            if self.ident == duenos:
                lista.append(index)
        self.Fabricante_cb.addItems(lista)
        self.LabsE_list.addItems(lista)

    def getProducto(self,lista):
        self.ProductosD_tb.clear()
        if lista == "productos":
            self.ProductosD_tb.setRowCount(0)
            self.ProductosD_tb.setColumnCount(0)
            length = self.db.llen(lista)
            print(length)
            productosL = []
            for i in range(length):
                index = self.db.lindex(lista,i)
                if self.db.hget(self.db.hget(index,"fabricante"),"jefe")==self.ident:
                    productosL.append(index)
                    self.ProductosD_tb.setRowCount(len(productosL))
            for i in range(len(productosL)):
                farm = self.db.hgetall(productosL[i])
                keys = farm.keys()
                self.ProductosD_tb.setColumnCount(len(keys))
                self.ProductosD_tb.setHorizontalHeaderLabels(keys)
                for j in range(len(keys)):
                    self.ProductosD_tb.setItem(
                        i, j, QtGui.QTableWidgetItem(str(farm[keys[j]]))
                    )

    def VentasR(self):
        pass

    def Pedidos(self):
        pass


    def __init__(self, ident):
        self.producto = {
            "id": "",
            "nombre": "",
            "fabricante": "",
            "costoVenta": "",
            "coste": "",
            "unidad": "",
            "seguridad": "",
            "familia": "",
        }
        self.laboratorio = {"id": "", "nombre": "", "productos": [], "jefe": ""}
        self.familia = {"nombre": ""}
        super(MainWindowLab, self).__init__()
        QtGui.QMainWindow.__init__(self)
        uic.loadUi("./ui/Laboratorio.ui", self)
        self.ident = ident
        self.db = redis.StrictRedis(
            host="159.89.34.186", password="papitopiernaslargas69", db=0, port="6379"
        )
        self.getFaricante()
        self.ListarLabs()
        self.getProducto("productos")
        self.getListFamilias()
        self.CrearP_bt.clicked.connect(partial(self.CrearP))
        self.pushButton_2.clicked.connect(partial(self.CrearLab))
        self.pushButton.clicked.connect(partial(self.CrearFamilia))
        self.pushButton.clicked.connect(partial(self.getListFamilias))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindowLab(0)
    window.show()
    sys.exit(app.exec_())
