
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from ui import main_design
import sys
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import scipy.io
from CodeDistribution import CodeDistribution
from PlotWindow import PlotWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = main_design.Ui_MainWindow()
        self.ui.setupUi(self)

        self.matfile = None
        self.ui.gbCoordinates.enabled = False
        self.ui.gbSWeighting.enabled = False

        self.plotDistWindow = PlotWindow()
        self.plotWDistWindow = PlotWindow()

        gm = [(0, 0, 0), (.15, .15, .5), (.3, .15, .75),
              (.6, .2, .50), (1, .25, .15), (.9, .5, 0),
              (.9, .75, .1), (.9, .9, .5), (1, 1, 1)]
        gerimap = LinearSegmentedColormap.from_list('GeriMap', gm)
        gerimap_r = LinearSegmentedColormap.from_list('GeriMap_r', gm[::-1])
        plt.register_cmap(cmap=gerimap)
        plt.register_cmap(cmap=gerimap_r)

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
            
            for var in self.matfile.keys():
                if not var.startswith('__'):
                    self.ui.cbVariable.addItem(var)

    def disableOptions(self):
        self.ui.gbCoordinates.setEnabled(False)
        self.ui.gbSWeighting.setEnabled(False)

    def enableOptions(self):
        self.ui.gbCoordinates.setEnabled(True)
        self.ui.gbSWeighting.setEnabled(True)

    def exit(self):
        self.plotDistWindow.close()
        self.plotWDistWindow.close()

    def loadFunction(self):
        varname = self.ui.cbVariable.currentText()

        os = self.matfile[varname]
        f = os[0,0]['f']
        y = os[0,0]['y'][0]
        delta = os[0,0]['delta'][0][0]
        Nxi = os[0,0]['Nxi'][0][0]
        #times = os[0,0]['times']

        if f.shape[1] > 1:
            print('Array contains distribution in several timesteps. Picking last timestep.')
            f = f[:,f.shape[1]-1]

        self.codedist = CodeDistribution(f, y, delta, Nxi)
        self.enableOptions()

        self.showPlots()

    def showPlots(self):
        if not self.plotDistWindow.isVisible():
            self.plotDistWindow.show()

        cd = self.codedist
        logf = np.log10(cd.f)

        PARAM1 = None
        PARAM2 = None

        if self.ui.rbPPitch.isChecked():
            PARAM1 = cd.THETA
            PARAM2 = cd.P
        else:
            PARAM1 = cd.PPAR
            PARAM2 = cd.PPERP

        self.plotDistWindow.plot(PARAM1, PARAM2, logf, cutoff=-9)

