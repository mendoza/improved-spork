import sys
reload(sys)
sys.setdefaultencoding('utf8')
import redis
from PyQt4 import QtCore, QtGui, uic

class MainWindowLab(QtGui.QMainWindow):

    def CrearP(self):
        ID = 0 #Lo hare incapaz de cambio
        Nombre = str(self.NombreP_edit.text())
        Fabricante = str(self.FabricanteP_cb.text())
        CostoVP = 0 #Cambiar a spinner
        CosteP = 0 #Cambiar a spinner
        UnidadP = int(self.Unidades_sp.value())
        SeguridadP = 0
        Familia = str(Familia_cb.text())

    def ListarLabs(self):
        
    def ListarProducto(self):

    def VentasR(self):

    def Pedidos(self):

    def ListaFamilias(self):

    def __init__(self):
        super(MainWindowLab, self).__init__()
        QtGui.QMainWindow.__init__(self)
        uic.loadUi("./ui/Laboratorio.ui", self)
        self.db = redis.StrictRedis(
            host="159.89.34.186", password="papitopiernaslargas69", db=0, port="6379"
        )

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindowLab()
    window.show()
    sys.exit(app.exec_())

