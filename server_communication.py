import sys
from PyQt5.QtWidgets import *#(QWidget, QToolTip, QPushButton, QLineEdit,
    #QPushButton, QApplication, QFrame, QInputDialog, QLabel)
from PyQt5.QtGui import *#QColor, QSizePolicy
from PyQt5.QtCore import *#QCoreApplication
from PyQt5.QtGui import *# QFont
import zmq
import diffie_hellman
import threading
from caesar_shifr import CaesarShifr


class ServerCommunicationMixin(object):

    def server_communication(self):
        self.server_communication_gui()
        chat_log_thread = threading.Thread(target=self.socket_logic_server)
        chat_log_thread.start()
        # self.socket_logic_server()

    def server_communication_gui(self):
        self.hide_last_objects()
        self.socket_port_server = "tcp://*:{}".format(self.input_port_server.text())

        label_port = QLabel("port  {}".format(self.socket_port_server), self)
        label_port.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label_port.setStyleSheet("QLabel {color: white;}")
        label_port.move(10, 12)

        self.label_general_secret_key_server = QLabel("_______________________", self)
        self.label_general_secret_key_server.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_general_secret_key_server.setStyleSheet("QLabel {color: white;}")
        self.label_general_secret_key_server.move(300, 80)
        label_general_key = QLabel("General_secret_key: ", self)
        label_general_key.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label_general_key.setStyleSheet("QLabel {color: white;}")
        label_general_key.move(170, 80)

        # CHAT
        white_frame = QFrame(self)
        color = QColor(255, 255, 255)
        white_frame.setStyleSheet("QWidget { background-color: %s }" % color.name())
        white_frame.setGeometry(0, 150, 600, 220) # x, y , width, height
        white_frame.show()
        self.label_chat_server = QLabel("_______________________________________________", self)
        self.label_chat_server.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_chat_server.setStyleSheet("QLabel {color: black;}")
        self.label_chat_server.move(20, 170)

        self.input_chat_server_phrase = QLineEdit(self)
        self.input_chat_server_phrase.move(20, 300)
        btn_send_phrase = QPushButton('send', self)
        btn_send_phrase.clicked.connect(self.server_send_phrase)
        btn_send_phrase.resize(btn_send_phrase.sizeHint())
        btn_send_phrase.move(250, 300)
        btn_send_phrase.show()
        #

        btn_exit = QPushButton('Quit', self)
        btn_exit.clicked.connect(QCoreApplication.instance().quit)

        btn_exit.resize(btn_exit.sizeHint())
        btn_exit.move(300, 470)
        btn_exit.show()

        btn_widget_choise = QPushButton('ago', self)
        btn_widget_choise.clicked.connect(self.server_set_socket_settings_gui)
        btn_widget_choise.resize(btn_exit.sizeHint())
        btn_widget_choise.move(30, 470)
        btn_widget_choise.show()

        self.objects_to_hide = (
            btn_exit, btn_widget_choise, btn_send_phrase,
            label_general_key, self.input_chat_server_phrase,
            label_port, white_frame, self.label_general_secret_key_server, self.label_chat_server
        )
        self.show_current_objects()

        self.setGeometry(200, 200, 400, 500)
        self.setWindowTitle('Server')
        self.show()

    def socket_logic_server(self):
        context = zmq.Context()
        self.server_socket = context.socket(zmq.REQ) # client / request
        print(self.socket_port_server)
        self.server_socket.bind(self.socket_port_server)

        general_secret_key_server = self.diffie_logic_server()
        self.caesar_shifr_server = CaesarShifr(general_secret_key_server)

    def diffie_logic_server(self):
        shared_prime = self.input_shared_prime_key_server.text()
        shared_base = self.input_shared_base_key_server.text()
        secret_key = self.input_seckret_key_server.text()
        
        diffie = diffie_hellman.DiffieHellman(shared_prime=shared_prime, shared_base=shared_base, secret_key=secret_key)
        server_medium_key = diffie.compute_medium_key()
        
        general_shared_keys = {'shared_prime': shared_prime, 'shared_base': shared_base, 'server_medium_key': server_medium_key}
        self.server_socket.send_json(general_shared_keys)
        
        client_middle_key = self.server_socket.recv_json()
        self.general_secret_key_server = diffie.compute_general_secret_key(client_middle_key['client_medium_key'])
        print(self.general_secret_key_server)
        self.label_general_secret_key_server.setText(str(self.general_secret_key_server))
        self.label_general_secret_key_server.show()

        return self.general_secret_key_server

    def server_send_phrase(self):

        if not hasattr(self, 'caesar_shifr_server'):
            self.label_chat_server.setText('МУДАК, КЛЮЧ НЕ ПОЛУЧЕН')
            return None

        text = self.input_chat_server_phrase.text()
        ecnryp_text = self.caesar_shifr_server.encryption(text)
        print(ecnryp_text)
        self.server_socket.send_json(ecnryp_text)
        
        client_encrypt_phrase = self.server_socket.recv_json()
        print(client_encrypt_phrase)
        client_phrase = self.caesar_shifr_server.decryption(client_encrypt_phrase)
        self.label_chat_server.setText(client_phrase)
        