import sys
reload(sys)
sys.setdefaultencoding('utf8')
import redis
from PyQt4 import QtCore, QtGui, uic
from functools import partial

    
class ui_registro(QtGui.QDialog):
    def signin(self):
        maistra = self.db.get("passwordadmin")
        # if aqui para validar :v
        
        length = self.db.llen("personas")
        lista = []
          
        for i in range(length):
            lista.append(self.db.lindex("personas", i))
        if self.id_edit.text() in lista:
            msg = QtGui.QMessageBox()
            msg.setIcon(QtGui.QMessageBox.Information)
            msg.setText("ID esta en lista")
            msg.setWindowTitle("ALERT")
            msg.setStandardButtons(QtGui.QMessageBox.Ok)
            msg.exec_()
        else:
            self.usuario["nombre"] = self.nombre_edit.text()
            self.usuario["direccion"] = self.direccion_edit.text()
            self.usuario["identidad"] = self.id_edit.text()
            self.usuario["edad"] = self.edad_spinner.value()
            self.usuario["password"] = self.password_edit.text()
            if maistra == self.ContraMaistra_edit.text():
                self.usuario["es_jefe"] = True  
            if self.masculino_rb.isChecked():
                self.usuario["sexo"] = "masculino"
            elif self.femenino_rb.isChecked():
                self.usuario["sexo"] = "femenino"
            elif self.otro_rb.isChecked():
                self.usuario["sexo"] = "otro"
            else:
                self.usuario["sexo"] = "N/A"
            if self.farmacia_rb.isChecked():
                self.usuario["departamento"] = "farmacia"
            elif self.laboratorio_rb.isChecked():
                self.usuario["departamento"] = "laboratorio"
            elif self.admin_rb.isChecked():
                self.usuario["departamento"] = "administracion"
            else:
                msg = QtGui.QMessageBox()
                msg.setIcon(QtGui.QMessageBox.Information)
                msg.setText("No se creo el usuario")
                msg.setWindowTitle("ALERT")
                msg.setStandardButtons(QtGui.QMessageBox.Ok)
                if msg.exec_():
                    return 

            self.db.hmset(self.usuario["identidad"], self.usuario)
            self.db.lpush("personas", self.usuario["identidad"])
            msg = QtGui.QMessageBox()
            msg.setIcon(QtGui.QMessageBox.Information)
            msg.setText("Funciono")
            msg.setWindowTitle("ALERT")
            msg.setStandardButtons(QtGui.QMessageBox.Ok)
            msg.exec_()


    def __init__(self):
        self.usuario = {
            "nombre": "",
            "edad": 1,
            "direccion": "",
            "identidad": "",
            "sexo": "",
            "password": "",
            "es_jefe":False,
            "departamento":""
        }
        super(ui_registro, self).__init__()
        QtGui.QMainWindow.__init__(self)
        uic.loadUi("./ui/signin.ui", self)
        self.db = redis.StrictRedis(
            host="159.89.34.186", password="papitopiernaslargas69", db=0, port="6379"
        )
        self.registro_bt.clicked.connect(partial(self.signin))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = ui_registro()
    window.show()
    sys.exit(app.exec_())