#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from PyQt5.QtWidgets import *
from gui import Ui_Widget


class Widgets(QWidget, Ui_Widget):
    """ Main Class """

    def __init__(self, parent=None):
        super(Widgets, self).__init__(parent)
        self.setupUi(self)
        self.btn1.clicked[bool].connect(self.editLabel)

    def editLabel(self):
        self.label.setText(self.inputText.text())

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    okno = Widgets()
    okno.show()

    sys.exit(app.exec_())