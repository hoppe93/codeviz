
from PyQt5 import QtWidgets
from ui import output_design
import numpy as np

class OutputWindow(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)

        self.ui = output_design.Ui_Output()
        self.ui.setupUi(self)

        self.bindEvents()

    def bindEvents(self):
        pass
