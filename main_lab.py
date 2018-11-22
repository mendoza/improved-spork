import sys

reload(sys)
sys.setdefaultencoding("utf8")
import redis
from PyQt4 import QtCore, QtGui, uic
from functools import partial


class MainWindowLab(QtGui.QMainWindow):
    def CrearP(self):
        self.Producto["id"] = "prod_" + str(self.db.get("contador_idproducto")).zfill(
            13
        )
        conta = int(float(self.db.get("contador_idproducto"))) + 1
        self.db.set("contador_idproducto", conta)
        self.producto["nombre"] = str(self.NombreP_edit.text())
        self.producto["fabricante"] = str(self.FabricanteP_cb.currentText())
        self.producto["costoVenta"] = int(self.CostoVenta_sp.value())
        self.producto["coste"] = int(self.Coste_sp.value())
        self.producto["unidad"] = int(self.Unidades_sp.value())
        SeguridadP = False
        if bool(self.Seguridad_cb.isTristate()):
            SeguridadP = True
        self.producto["seguridad"] = bool(SeguridadP)
        self.producto["familia"] = str(self.Familia_cb.currentText())
        self.db.lpush("productos",self.producto["id"])
        self.db.hmset(self.producto["id"],self.producto)
        
    def CrearLab(self):
        self.laboratorio["id"] = "lab_" + str(self.db.get("contador_idLab")).zfill(13)
        conta = int(float(self.db.get("contador_idLab"))) + 1
        self.db.set("contador_idLab", conta)
        self.laboratorio["nombre"] = str(self.NombreL_edit.text())
        self.laboratorio["direccion"] = str(self.DireccionL.text())
        self.laboratorio["jefe"] = self.ident
        self.db.lpush("laboratorios",self.laboratorio["id"])
        self.db.hmset(self.laboratorio["id"],self.laboratorio)
    def CrearFamilia(self):
        famP = str(self.Familia.edit.text())
        self.db.lpush("familias",famP)
        self.getListFamilias()

    def getListFamilias(self):
        self.Familia_cb.clear()
        length = self.db.llen("familias")
        lista = []
        for i in range(length):
            index = self.db.lindex("familias", i)
            lista.append(index)
        self.Familia_cb.addItems(lista)

    def getFaricante(self):
        self.Fabricante_cb.clear()
        length = self.db.llen("laboratorios")
        lista2 = []
        for i in range(length):
            index = self.db.lindex("laboratorios",i)
            lista2.append(index)
        self.Fabricante_cb.addItems(lista2)

    def ListarLabs(self):
        length = self.db.llen("labs")
        lista = []
        for i in range(length):
            index = self.db.lindex("labs", i)
            duenos = self.db.hmget(index, "duenos")[0].replace("[", "")
            duenos = duenos.replace("]", "")
            duenos = duenos.replace("'", "")
            duenos = duenos.split(",")
            if self.ident in duenos:
                lista.append(index)
        self.Fabricante_cb.addItems(lista)

    def getProducto(self,lista):
        self.ProductosD_tb.clear()
        if lista == "producto":
            self.verfarm_tb.setRowCount(0)
            self.verfarm_tb.setColumnCount(0)
            length = self.db.llen(lista)
            print(length)
            productosL = []
            for i in range(length):
                index = self.db.lindex(lista,i)
                produc = self.db.hmget(index, "productos")[0].replace("[", "")
                produc = produc.replace("]", "")
                produc = produc.replace("'", "")
                produc = duenos.split(",")                        

    def VentasR(self):
        pass

    def Pedidos(self):
        pass

    def ListaFamilias(self):
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

        self.CrearP_bt.clicked.connect(partial(self.CrearP))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindowLab(0)
    window.show()
    sys.exit(app.exec_())
