# -*- coding: utf-8 -*-
import socket
import time
# 192.168.1.12

from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
import tetris

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(370, 573)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 40, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka Subheading Semibold")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(150, 150, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(150, 210, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(150, 280, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(100, 180, 171, 16))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(100, 250, 171, 16))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(100, 320, 171, 16))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(110, 390, 151, 91))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 370, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Вход в игру"))
        self.label_2.setText(_translate("MainWindow", "IP адрес"))
        self.label_3.setText(_translate("MainWindow", "Никнейм"))
        self.label_4.setText(_translate("MainWindow", "Пароль"))
        self.pushButton.setText(_translate("MainWindow", "ВХОД"))


class Window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.score = 0
        app.aboutToQuit.connect(self.closeEvent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.connect)

    def ip_check(self):
        row = self.lineEdit.text()
        a = row.split(":")
        self.ip = a[0].split(".")
        self.port = a[1]
        if not (self.port.isnumeric() and 1024 <= int(self.port) <= 65535):
            return False
        for byte in self.ip:
            if not (byte.isnumeric() and 0 <= int(byte) <= 255):
                return False
        return True

    def empty_check(self):
        self.name = self.lineEdit_2.text()
        self.pasw = self.lineEdit_3.text()
        log = [False, False]
        if not self.name == "":
            log[0] = True
        if not self.pasw == "":
            log[1] = True
        return log

    def showEvent(self, event):
        print(self.score)
        if self.score == 0:
            return

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        try:
            sock.connect((self.ip, self.port))
            info = f"<final,{self.name},{self.pasw},{self.score}>".encode()
            sock.send(info)
        except:
            print("Не смог подключиться")
            return

    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        empty = self.empty_check()
        if not all(empty):
            print("Поля пустые!")
            return

        if not self.ip_check():
            print("IP-адрес не верен!")
            return
        self.ip = ".".join(self.ip)
        self.port = int(self.port)

        try:
            sock.connect((self.ip, self.port))
            info = f"<{self.name},{self.pasw}>".encode()
            sock.send(info)
        except Exception as e:
            print("Не смог подключиться", e)
            return
        tick = 0
        while True:
            try:
                data = sock.recv(1024).decode()
                data = find(data)
                if int(data[0]) >= 0:
                    self.record = data[0]
                    self.start_game()
                    return
                elif data[0] == "-1":
                    wrong = QMessageBox(text = "Неправильный пароль. Попробуйте ещё раз.", )
                    wrong.setWindowTitle("Внимание!")
                    wrong.setText("Неправильный пароль. Попробуйте ещё раз.")
                    wrong.setIcon(QMessageBox.Icon.Warning)
                    wrong.setStyleSheet("color: black")
                    wrong.exec()
                    return
                else:
                    return

            except:
                tick += 1
                time.sleep(0.5)
                if tick == 20:
                    return

    def start_game(self):
        self.tetris = tetris.Tetris(self, app)
        self.tetris.setStyleSheet("background-color: black")
        self.tetris.show()
        self.close()

def find(data):

    first = None
    for num, sign in enumerate(data):
        if sign == "<":
            first = num
        if sign == ">" and first is not None:
            second = num

            result = data[first + 1:second].split(",")
    return result
stylesheet = """ 
    QMainWindow { 
            border-image: url(tetris.jpg) 0 0 0 0 stretch stretch; 
    }
     QLabel {
     color: white

     }"""
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    w = Window()
    app.setStyleSheet(stylesheet)

    w.show()
    # MainWindow = QtWidgets.QMainWindow()
    # ui = Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    sys.exit(app.exec())
