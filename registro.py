import sys
import redis
from PyQt4 import QtCore, QtGui, uic
from functools import partial

    
class ui_registro(QtGui.QDialog):
    def signin(self):
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
            if self.rb_masculino.isChecked():
                self.usuario["sexo"] = "masculino"
            elif self.rb_femenino.isChecked():
                self.usuario["sexo"] = "femenino"
            elif self.rb_otro.isChecked():
                self.usuario["sexo"] = "otro"
            else:
                self.usuario["sexo"] = "N/A"
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
        }
        super(ui_registro, self).__init__()
        QtGui.QMainWindow.__init__(self)
        uic.loadUi("./ui/signin.ui", self)
        self.db = redis.StrictRedis(
            host="159.89.34.186", password="papitopiernaslargas69", db=0, port="6379"
        )
        self.bt_registro.clicked.connect(partial(self.signin))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = ui_registro()
    window.show()
    sys.exit(app.exec_())

"""import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)
for key in r.scan_iter("user:*"):
    # delete the key
    r.delete(key)"""