
from PyQt5 import QtWidgets
from ui import grid_design
import numpy as np

class GridWindow(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)

        self.ui = grid_design.Ui_Grid()
        self.ui.setupUi(self)

        self.f = None
        self.X = None
        self.Y = None
        self.coordinates = 'p'
        self.normalizedUnits = True
        self.thresholds = {
            '50%': 5e-1,
            '20%': 2e-1,
            '10%': 1e-1,
            '5%': 5e-2,
            '2%': 2e-2,
            '1%': 1e-2,
            '0.5%': 5e-3,
            '0.2%': 2e-3,
            '0.1%': 1e-3,
            '0.05%': 5e-4,
            '0.02%': 2e-4,
            '0.01%': 1e-4
        }

        self.mc = 0.5109989461

        self.bindEvents()

    def bindEvents(self):
        self.ui.btnOptimize.clicked.connect(self.optimize)

    def optimize(self):
        WF = self.f
        PARAM1 = self.X
        PARAM2 = self.Y
        WF[WF < self.threshold] = 10

        if self.normalizedUnits:
            PARAM1 = PARAM1 * self.mc
            PARAM2 = PARAM2 * self.mc

        param1max, param1min = 0, np.amax(PARAM1)
        param2max, param2min = 0, np.amax(PARAM2)
        valmin = 10

        ni, nj = WF.shape

        # Find parameter bounds
        for i in range(0, ni-1):
            for j in range(0, nj-1):
                if WF[i,j] < 10:
                    if PARAM1[i,j] > param1max:
                        param1max = PARAM1[i,j]
                    if PARAM1[i,j] < param1min:
                        param1min = PARAM1[i,j]

                    if PARAM2[i,j] > param2max:
                        param2max = PARAM2[i,j]
                    if PARAM2[i,j] < param2min:
                        param2min = PARAM2[i,j]

        # Set boundary labels on dialog
        self.ui.lblParam1Start.setText('%.2f MeV/c' % param1min)
        self.ui.lblParam1End.setText('%.2f MeV/c' % param1max)
        self.ui.lblParam2Start.setText('%.2f MeV/c' % param2min)
        self.ui.lblParam2End.setText('%.2f MeV/c' % param2max)

        # Distribute points
        points = int(self.ui.tbPoints.text())
        param1n, param2n = 0, 0
        #if self.coordinates == 'p':
        n = np.floor(np.sqrt(points))
        if n % 2 == 1:
            if n > 2: n = n - 1
            else: n = 2

        param1n = n
        param2n = n
        if self.coordinates == 'p':
            self.ui.tbSOFT.setPlainText('pitch=%.2f,%.2f,%d;\np=%.2f,%.2f,%d;' % (param1min, param1max, param1n, param2min, param2max, param2n))
        elif self.coordinates == 'ppar':
            self.ui.tbSOFT.setPlainText('ppar=%.2f,%.2f,%d;\npperp=%.2f,%.2f,%d;' % (param1min, param1max, param1n, param2min, param2max, param2n))

        self.ui.lblParam1N.setText('%d' % param1n)
        self.ui.lblParam2N.setText('%d' % param2n)

        self.param1min = param1min
        self.param1max = param1max
        self.param1n   = param1n
        self.param2min = param2min
        self.param2max = param2max
        self.param2n   = param2n

        self.ui.btnVisualize.setEnabled(True)

    def setThreshold(self, threshold):
        self.threshold = threshold

    def showEvent(self, event):
        if self.coordinates == 'p':
            self.ui.lblNameParam1.setText('pitch')
            self.ui.lblNameParam2.setText('p')
            self.ui.tbSOFT.setPlainText('pitch=0,0,0;\np=0,0,0;')
        elif self.coordinates == 'ppar':
            self.ui.lblNameParam1.setText('ppar')
            self.ui.lblNameParam2.setText('pperp')
            self.ui.tbSOFT.setPlainText('ppar=0,0,0;\npperp=0,0,0;')
        else:
            raise ValueError('Unrecognized coordinate type: '+self.coordinates)

