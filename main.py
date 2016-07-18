# -*- codung:utf-8 -*-
import sys
from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication, QFrame)
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QColor

import client_settings
import server_settings


class MainWidget(client_settings.ClientSetSocketSettingsMixin, server_settings.ServerSetSocketSettingsMixin, QWidget):

    def __init__(self):
        super().__init__()
        self.objects_to_hide = () # list objects who must be hided in nest layer
        self.start_GUI()
        
    def start_GUI(self):
        frm = QFrame(self)
        col = QColor(0, 0, 0)
        frm.setStyleSheet("QWidget { background-color: %s }" % col.name())
        frm.setGeometry(0, 0, 800, 800)
        frm.show()
        self.gui_choise_server_client()

    def gui_choise_server_client(self):
        self.hide_last_objects()

        QToolTip.setFont(QFont('SansSerif', 10))

        btn_server = QPushButton('Server', self)
        btn_server.clicked.connect(self.server_set_socket_settings_gui) # from server.ServerMixin TODO аналогично
        btn_server.resize(btn_server.sizeHint())
        btn_server.move(50, 50)


        btn_client = QPushButton('Client', self)
        btn_client.clicked.connect(self.client_set_socket_settings_gui) # from client.ClientMixin
        btn_client.resize(btn_client.sizeHint())
        btn_client.move(150, 50)

        btn_exit = QPushButton('Quit', self)
        btn_exit.clicked.connect(QCoreApplication.instance().quit)
        btn_exit.resize(btn_exit.sizeHint())
        btn_exit.move(200, 170)

        self.setGeometry(450, 300, 300, 200)
        self.setWindowTitle('Client_Server')
        self.show()

        self.objects_to_hide = (btn_exit, btn_client, btn_server)
        self.show_current_objects()

    # TOOLS for hide/show objects
    def hide_last_objects(self):  # all objects created in layer must be hided
        for obj in self.objects_to_hide:
            obj.hide()

    def show_current_objects(self):
        for obj in self.objects_to_hide:
            obj.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWidget()
    sys.exit(app.exec_())