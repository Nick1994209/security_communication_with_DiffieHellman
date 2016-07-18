import sys
from PyQt5.QtWidgets import *#(QWidget, QToolTip, QPushButton, QLineEdit,
    #QPushButton, QApplication, QFrame, QInputDialog, QLabel)
from PyQt5.QtGui import *#QColor, QSizePolicy
from PyQt5.QtCore import *#QCoreApplication
from PyQt5.QtGui import *# QFont
import random
import zmq
import diffie_hellman
import threading
from caesar_shifr import CaesarShifr


class ClientCommunicationMixin(object):

    def client_communicatoin(self):
        self.client_communication_gui()
        chat_log_thread = threading.Thread(target=self.socket_logic_client)
        chat_log_thread.start()
        #self.socket_logic_client()

    def client_communication_gui(self):
        self.hide_last_objects()
        port = int(self.input_port_client.text())
        ip = self.input_ip_client.text()
        self.client_socket_port = "tcp://{0}:{1}".format(ip, port)

        label_socket_port = QLabel("port  {}".format(self.client_socket_port), self)
        label_socket_port.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label_socket_port.setStyleSheet("QLabel {color: white;}")
        label_socket_port.move(10, 12)

        self.label_general_secret_key_client = QLabel("_______________", self)
        self.label_general_secret_key_client.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_general_secret_key_client.setStyleSheet("QLabel {color: white;}")
        self.label_general_secret_key_client.move(300, 80)
        label_general_key = QLabel("General_secret_key: ", self)
        label_general_key.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label_general_key.setStyleSheet("QLabel {color: white;}")
        label_general_key.move(170, 80)

        # chat
        white_frame = QFrame(self)
        color = QColor(255, 255, 255)
        white_frame.setStyleSheet("QWidget { background-color: %s }" % color.name())
        white_frame.setGeometry(0, 150, 600, 180)
        white_frame.show()
        self.label_chat_client = QLabel("_______________________________________________", self)
        self.label_chat_client.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_chat_client.setStyleSheet("QLabel {color: black;}")
        self.label_chat_client.move(20, 170)

        self.input_chat_client_phrase = QLineEdit(self)
        self.input_chat_client_phrase.move(20, 300)
        btn_send_phrase = QPushButton('send to server', self)
        btn_send_phrase.clicked.connect(self.client_send_phrase)
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
        btn_widget_choise.clicked.connect(self.client_set_socket_settings_gui)
        btn_widget_choise.resize(btn_exit.sizeHint())
        btn_widget_choise.move(30, 470)
        btn_widget_choise.show()

        self.objects_to_hide = (btn_exit, btn_widget_choise, label_socket_port, label_general_key, white_frame,
                                btn_send_phrase, self.input_chat_client_phrase,
                                self.label_general_secret_key_client, self.label_chat_client)
        self.show_current_objects()

        self.setGeometry(800, 200, 400, 500)
        self.setWindowTitle('Client')
        self.show()

    def socket_logic_client(self):
        context = zmq.Context()
        self.client_socket = context.socket(zmq.REP) # server / reply
        self.client_socket.connect(self.client_socket_port)

        general_secret_key_client = self.diffie_logic_client()
        self.cesar_shifr_client = CaesarShifr(general_secret_key_client)

        self.getting_phrases_from_server()

    def diffie_logic_client(self):
        # server sended : shared_prime, shared_base and server_medium_key
        general_shared_keys = self.client_socket.recv_json()
        print(general_shared_keys)
        print(general_shared_keys)
        shared_prime = general_shared_keys['shared_prime']
        shared_base = general_shared_keys['shared_base']
        secret_key = self.input_seckret_key_client.text()

        diffie = diffie_hellman.DiffieHellman(shared_prime=shared_prime, shared_base=shared_base, secret_key=secret_key)
        client_medium_key = diffie.compute_medium_key()
        client_medium_key = {'client_medium_key': client_medium_key}
        self.client_socket.send_json(client_medium_key)

        # compute general secret key
        self.general_secret_key_client = diffie.compute_general_secret_key(general_shared_keys['server_medium_key'])
        print(self.general_secret_key_client)
        self.label_general_secret_key_client.setText(str(self.general_secret_key_client))
        self.label_general_secret_key_client.show()

        return self.general_secret_key_client

    def getting_phrases_from_server(self):
        if not hasattr(self, 'cesar_shifr_client'):
            self.label_chat_client.setText('МУДАК, КЛЮЧ НЕ ПОЛУЧЕН')
            return

        server_shifr_phrase = self.client_socket.recv_json()
        server_phrase = self.cesar_shifr_client.decryption(server_shifr_phrase)
        self.label_chat_client.setText(server_phrase)

    def client_send_phrase(self):
        if not hasattr(self, 'cesar_shifr_client'):
            self.label_chat_client.setText('МУДАК, КЛЮЧ НЕ ПОЛУЧЕН')
            return

        client_phrase = self.input_chat_client_phrase.text()
        shifr_client_phrase = self.cesar_shifr_client.encryption(client_phrase)
        self.client_socket.send_json(shifr_client_phrase)
