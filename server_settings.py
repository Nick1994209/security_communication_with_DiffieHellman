import sys
from PyQt5.QtWidgets import *#(QWidget, QToolTip, QPushButton, QLineEdit,
    #QPushButton, QApplication, QFrame, QInputDialog, QLabel)
from PyQt5.QtGui import *#QColor, QSizePolicy
from PyQt5.QtCore import *#QCoreApplication
from PyQt5.QtGui import *# QFont
import random
from server_communication import ServerCommunicationMixin


class ServerSetSocketSettingsMixin(ServerCommunicationMixin):

    def server_set_socket_settings_gui(self):
        self.hide_last_objects()

        self.input_port_server = QLineEdit(self)
        self.input_port_server.move(40, 10)
        label_port = QLabel("port", self)
        label_port.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label_port.setStyleSheet("QLabel {color: white;}")
        label_port.move(2, 12)

        self.input_seckret_key_server = QLineEdit(self)
        self.input_seckret_key_server.move(40, 50)
        label_secret_key = QLabel("key", self)
        label_secret_key.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label_secret_key.setStyleSheet("QLabel {color: white;}")
        label_secret_key.move(2, 52)
        btn_secret_key = QPushButton('random_secret_key', self)
        btn_secret_key.clicked.connect(self.random_server_key)
        btn_secret_key.resize(btn_secret_key.sizeHint())
        btn_secret_key.move(200, 50)

        self.input_shared_base_key_server = QLineEdit(self)
        self.input_shared_base_key_server.move(40, 100)
        label_shared_base_key = QLabel("base", self)
        label_shared_base_key.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label_shared_base_key.setStyleSheet("QLabel {color: white;}")
        label_shared_base_key.move(2, 102)
        btn_shared_base_key = QPushButton('random_general_key', self)
        btn_shared_base_key.clicked.connect(self.random_shared_key)
        btn_shared_base_key.resize(btn_secret_key.sizeHint())
        btn_shared_base_key.move(200, 100)

        self.input_shared_prime_key_server = QLineEdit(self)
        self.input_shared_prime_key_server.move(40, 150)
        label_shared_prime_key = QLabel("prime", self)
        label_shared_prime_key.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label_shared_prime_key.setStyleSheet("QLabel {color: white;}")
        label_shared_prime_key.move(2, 152)
        btn_shared_prime_key = QPushButton('random_prime_key', self)
        btn_shared_prime_key.clicked.connect(self.random_prime_key)
        btn_shared_prime_key.resize(btn_secret_key.sizeHint())
        btn_shared_prime_key.move(200, 150)

        self.label_digit_field = QLabel("", self)
        self.label_digit_field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_digit_field.setStyleSheet("QLabel {color: white;}")
        self.label_digit_field.move(100, 200)

        btn_next = QPushButton('next', self)
        btn_next.clicked.connect(self.next_server_window)
        btn_next.resize(btn_next.sizeHint())
        btn_next.move(180, 270)

        btn_exit = QPushButton('Quit', self)
        btn_exit.clicked.connect(QCoreApplication.instance().quit)
        btn_exit.resize(btn_exit.sizeHint())
        btn_exit.move(300, 270)
        btn_exit.show()

        btn_widget_choise = QPushButton('ago', self)
        btn_widget_choise.clicked.connect(self.gui_choise_server_client)
        btn_widget_choise.resize(btn_exit.sizeHint())
        btn_widget_choise.move(30, 270)
        btn_widget_choise.show()

        self.objects_to_hide = (
            btn_exit, btn_widget_choise, btn_next, btn_secret_key, btn_shared_base_key, btn_shared_prime_key,
            label_port, label_secret_key, label_shared_base_key, label_shared_prime_key, self.label_digit_field,
            self.input_port_server, self.input_seckret_key_server, self.input_shared_base_key_server, self.input_shared_prime_key_server
        )
        self.show_current_objects()

        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('ServerSettings')
        self.show()

    def random_server_key(self):
        self.input_seckret_key_server.setText(str(random.randint(0, 10000)))

    def random_shared_key(self):
        self.input_shared_base_key_server.setText(str(random.randint(0, 10000)))

    def random_prime_key(self):
        self.input_shared_prime_key_server.setText(str(random.randint(0, 10000)))

    def next_server_window(self):
        if self.input_port_server.text() and self.input_seckret_key_server.text() and self.input_shared_base_key_server.text()\
                and self.input_shared_prime_key_server.text():
            if self.input_port_server.text().isdigit():
                self.server_communication()
            else:
                self.label_digit_field.hide()
                self.label_digit_field.setText('Port must be integer')
                self.label_digit_field.show()
        else:
            self.label_digit_field.hide()
            self.label_digit_field.setText('All fields value must be filled')
            self.label_digit_field.show()

