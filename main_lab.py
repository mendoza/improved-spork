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
        CostoVP = 0  # Cambiar a spinner
        CosteP = 0  # Cambiar a spinner
        UnidadP = int(self.Unidades_sp.value())
        SeguridadP = 0
        Familia = str(self.Familia_cb.text())

    def ListarLabs(self):
        pass

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
