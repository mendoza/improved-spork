import sys

reload(sys)
sys.setdefaultencoding("utf8")
import redis
from PyQt4 import QtCore, QtGui, uic


class MainWindowLab(QtGui.QMainWindow):
    def CrearP(self):
        Iden = 0  # Lo hare incapaz de cambio
        Nombre = str(self.NombreP_edit.text())
        Fabricante = str(self.FabricanteP_cb.text())
        CostoVP = int(self.CostoVenta_sp.value())
        CosteP = int(self.Coste_sp.value())
        UnidadP = int(self.Unidades_sp.value())
        SeguridadP = False
        if(bool(self.Seguridad_cb.isTristate())):
            SeguridadP = True
        Familia = str(self.Familia_cb.text())

    def ListarLabs(self):
        length = self.db.llen("labs")
        lista = []
        for i in range(length):
            index =self.db.lindex("labs",i)
            duenos = self.db.hmget(index,"duenos")[0].replace('[','')
            duenos = duenos.replace(']','')
            duenos = duenos.replace('\'','')
            duenos = duenos.split(',')
            if self.ident in duenos:
                lista.append(index)
        self.eliminarfarm_cb.addItems(lista)

    def ListarProducto(self):
        pass

    def VentasR(self):
        pass

    def Pedidos(self):
        pass

    def ListaFamilias(self):
        pass

    def __init__(self, ident):
        super(MainWindowLab, self).__init__()
        QtGui.QMainWindow.__init__(self)
        uic.loadUi("./ui/Laboratorio.ui", self)
        self.ident = ident
        self.db = redis.StrictRedis(
            host="159.89.34.186", password="papitopiernaslargas69", db=0, port="6379"
        )


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindowLab(0)
    window.show()
    sys.exit(app.exec_())
