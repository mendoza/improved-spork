# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding("utf8")
import redis
from PyQt4 import QtCore, QtGui, uic
from functools import partial
import hashlib
from registro import ui_registro
from main_farmacia import MainWindowFarmacia
from main_lab import MainWindowLab
from main_bodega import MainWindowBodega

"""me gusta las piernas de papitopiernaslargas69"""


class InicioWindow(QtGui.QDialog):
    def login(self):
        identidad = "per_"+str(self.id_edit.text()).zfill(13)
        print(identidad)
        password = str(self.password_edit.text())
        if self.existencia("personas", identidad) == True:
            print("entre :V")
            if (
                str(self.db.hmget(identidad, "identidad")
                    [0]) ==identidad
                and str(self.db.hmget(identidad, "password")[0]) == password
            ):
                msg = QtGui.QMessageBox()
                msg.setIcon(QtGui.QMessageBox.Information)
                msg.setText("Bienvenido " + identidad)
                msg.setWindowTitle("Ingreso Exiosamente")
                msg.setStandardButtons(QtGui.QMessageBox.Ok)
                if msg.exec_():
                    print(self.db.hmget(identidad, "trabaja")[0])
                    if (self.db.hmget(identidad, "departamento")[0] == "farmacia") and (self.db.hmget(identidad,"trabaja")[0] == "True"):
                        window = QtGui.QMainWindow()
                        print("entro")
                        ui = MainWindowFarmacia(identidad)
                        ui.show()
                        self.close()
                        sys.exit(ui.exec_())
                    elif self.db.hmget(identidad, "departamento")[0] == "laboratorio":
                        window = QtGui.QMainWindow()
                        ui = MainWindowLab(identidad)
                        ui.show()
                        self.close()
                        sys.exit(ui.exec_())
                    elif self.db.hmget(identidad, "departamento")[0] == "bodega":
                        window = QtGui.QMainWindow()
                        ui = MainWindowBodega(identidad)
                        ui.show()
                        self.close()
                        sys.exit(ui.exec_())
                    elif (self.db.hmget(identidad, "departamento")[0] == "farmacia") and (self.db.hmget(identidad,"trabaja")[0] != "True"):
                        msg = QtGui.QMessageBox()
                        msg.setIcon(QtGui.QMessageBox.Information)
                        msg.setText("Lo siento no cumple los requisitos " + identidad)
                        msg.setWindowTitle("Sorry not Srry")
                        msg.setStandardButtons(QtGui.QMessageBox.Ok)
                        msg.exec_()
                    else:
                        return
            else:
                print("no entro")
        else:
            print("no existe")

    def signin(self):
        Dialog = QtGui.QDialog()
        ui = ui_registro()
        ui.show()
        ui.exec_()
   
        
    def existencia(self, nlista, iden):
        length = self.db.llen(nlista)
        lista = []
        if length == 0:
            return False
        else:
            for i in range(length):
                lista.append(self.db.lindex(nlista, i))
            return iden in lista

    def __init__(self):
        super(InicioWindow, self).__init__()
        QtGui.QMainWindow.__init__(self)
        uic.loadUi("./ui/login.ui", self)
        self.db = redis.StrictRedis(
            host="159.89.34.186", password="papitopiernaslargas69"
        )
        self.bt_login.clicked.connect(partial(self.login))
        self.bt_signin.clicked.connect(partial(self.signin))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = InicioWindow()
    window.show()
    sys.exit(app.exec_())
