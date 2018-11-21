import sys

reload(sys)
sys.setdefaultencoding("utf8")
import redis
from PyQt4 import QtCore, QtGui, uic
from functools import partial


class MainWindowLab(QtGui.QMainWindow):
    def CrearP(self):
        self.Producto["id"] = "prod_" + \
            str(self.db.get("contador_idproducto")).zfill(13)
        conta = int(float(self.db.get("contador_idproducto"))) + 1
        self.db.set("contador_idproducto", conta)
        self.Producto["nombre"] = str(self.NombreP_edit.text())
        self.Producto["fabricante"] = str(self.FabricanteP_cb.text())
        self.Producto["costoVP"] = int(self.CostoVenta_sp.value())
        self.Producto["costeP"] = int(self.Coste_sp.value())
        self.Producto["unidadP"] = int(self.Unidades_sp.value())
        SeguridadP = False
        if bool(self.Seguridad_cb.isTristate()):
            SeguridadP = True
        self.Producto["seguridadP"] = bool(SeguridadP)
        Familia = str(self.Familia_cb.text())

    def CrearLab(self):
        self.Laboratorio["id"] = "lab" + \
            str(self.db.get("contador_idLab")).zfill(13)
        conta = int(float(self.db.get("contador_idLab"))) + 1
        self.db.set("contador_idLab", conta)
        self.Laboratorio["nombre"] = str(self.NombreL_edit.text())
        self.Laboratorio["direccion"] = str(self.DireccionL.text())

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

    def ListarProducto(self):
        pass

    def VentasR(self):
        pass

    def Pedidos(self):
        pass

    def ListaFamilias(self):
        pass

    def __init__(self, ident):
        self.Producto = {
            "id": "",
            "nombre": "",
            "fabricante": "",
            "costoVenta": "",
            "coste": "",
            "unidad": "",
            "seguridad": "",
            "familia": "",
        }
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
