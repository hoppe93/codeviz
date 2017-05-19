
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from ui import main_design
import sys
import numpy as np
import scipy.io

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = main_design.Ui_MainWindow()
        self.ui.setupUi(self)

        self.matfile = None
        self.ui.gbCoordinates.enabled = False
        self.ui.gbSWeighting.enabled = False

        self.bindEvents()

    def bindEvents(self):
        self.ui.btnBrowse.clicked.connect(self.browseFile)
        self.ui.btnLoad.clicked.connect(self.loadFunction)

    def browseFile(self):
        filename, _ = QFileDialog.getOpenFileName(parent=self, caption="Open CODE distribution", filter="CODE Distribution (*.mat);;All files (*.*)")

        if filename:
            self.ui.tbFunction.setText(filename)
            self.matfile = scipy.io.loadmat(filename)
            self.ui.cbVariable.clear()
            
            #for var in self.matfile.keys():
            for var in self.matfile.keys():
                if not var.startswith('__'):
                    self.ui.cbVariable.addItem(var)

    def disableOptions(self):
        self.ui.gbCoordinates.setEnabled(False)
        self.ui.gbSWeighting.setEnabled(False)

    def enableOptions(self):
        self.ui.gbCoordinates.setEnabled(True)
        self.ui.gbSWeighting.setEnabled(True)

    def loadFunction(self):
        self.enableOptions()
