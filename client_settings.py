import sys
from PyQt5.QtWidgets import *#(QWidget, QToolTip, QPushButton, QLineEdit,
    #QPushButton, QApplication, QFrame, QInputDialog, QLabel)
from PyQt5.QtGui import *#QColor, QSizePolicy
from PyQt5.QtCore import *#QCoreApplication
from PyQt5.QtGui import *# QFont
import random
from client_communication import ClientCommunicationMixin


class ClientSetSocketSettingsMixin(ClientCommunicationMixin):

    def client_set_socket_settings_gui(self):
        self.hide_last_objects()

        self.input_port_client = QLineEdit(self)
        self.input_port_client.move(40, 10)
        label_port = QLabel("port", self)
        label_port.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label_port.setStyleSheet("QLabel {color: white;}")
        label_port.move(0, 12)

        self.input_ip_client = QLineEdit(self)
        self.input_ip_client.move(200, 10)
        self.input_ip_client.setText('localhost')

        label_ip = QLabel("ip", self)
        label_ip.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label_ip.setStyleSheet("QLabel {color: white;}")
        label_ip.move(180, 12)

        self.input_seckret_key_client = QLineEdit(self)
        self.input_seckret_key_client.move(40, 50)
        label_secret_key = QLabel("key", self)
        label_secret_key.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label_secret_key.setStyleSheet("QLabel {color: white;}")
        label_secret_key.move(0, 50)
        btn_secret_key = QPushButton('random_secret_key', self)
        btn_secret_key.clicked.connect(self.random_servet_key)
        btn_secret_key.resize(btn_secret_key.sizeHint())
        btn_secret_key.move(200, 50)

        btn_next = QPushButton('next', self)
        btn_next.clicked.connect(self.next_client_window)
        btn_next.resize(btn_next.sizeHint())
        btn_next.move(180, 170)

        btn_exit = QPushButton('Quit', self)
        btn_exit.clicked.connect(QCoreApplication.instance().quit)
        btn_exit.resize(btn_exit.sizeHint())
        btn_exit.move(300, 170)
        btn_exit.show()

        btn_widget_choise = QPushButton('ago', self)
        btn_widget_choise.clicked.connect(self.gui_choise_server_client)
        btn_widget_choise.resize(btn_exit.sizeHint())
        btn_widget_choise.move(30, 170)
        btn_widget_choise.show()

        self.objects_to_hide = (
            btn_exit, btn_widget_choise, btn_next, btn_secret_key,
            label_port, label_ip, label_secret_key,
            self.input_port_client, self.input_ip_client, self.input_seckret_key_client
        )
        self.show_current_objects()

        self.setGeometry(600, 300, 400, 200)
        self.setWindowTitle('Client')
        self.show()

    def random_servet_key(self):
        self.input_seckret_key_client.setText(str(random.randint(0, 10000)))

    def next_client_window(self):
        if self.input_port_client.text() and self.input_ip_client.text() and self.input_seckret_key_client.text():
            if self.input_port_client.text().isdigit():
                self.client_communicatoin()