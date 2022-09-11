#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from PyQt5.QtWidgets import *


class Ui_Widget(object):
    """ GUI Class"""

    def setupUi(self, Widget):
        layoutMain = QVBoxLayout()
        layout1 = QHBoxLayout()
        self.label = QLabel('Input some text:')
        self.inputText = QLineEdit()
        self.btn1 = QPushButton('Enter')
        layout1.addWidget(self.label)
        layout1.addWidget(self.inputText)
        layout1.addWidget(self.btn1)
        

        layoutMain.addLayout(layout1)
        self.setLayout(layoutMain)
        self.setWindowTitle('Widgets')