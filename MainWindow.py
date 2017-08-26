
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
from GridWindow import GridWindow
from OutputWindow import OutputWindow

class MainWindow(QtWidgets.QMainWindow):
    mc = 0.5109989461

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = main_design.Ui_MainWindow()
        self.ui.setupUi(self)

        self.matfile = None
        self.ui.gbCoordinates.setEnabled(False)
        self.ui.gbSWeighting.setEnabled(False)

        self.plotDistWindow = PlotWindow()
        self.plotWeightWindow = PlotWindow()
        self.gridWindow = GridWindow()
        self.exportWindow = OutputWindow()
        self.WF = None

        self.spectrumPresets = [
            {'name': 'Alcator C-Mod', 'low': 400, 'lowunit': 'nm', 'up': 800, 'upunit': 'nm', 'B': 7.13},
            {'name': 'ASDEX-U IR', 'low': 3, 'lowunit': 'µm', 'up': 5, 'upunit': 'µm', 'B': 3},
            {'name': 'DIII-D Visible', 'low': 740, 'lowunit': 'nm', 'up': 760, 'upunit': 'nm', 'B': 2},
            {'name': 'DIII-D IR', 'low': 3, 'lowunit': 'µm', 'up': 5, 'upunit': 'µm', 'B': 2},
            {'name': 'REIS', 'low': 400, 'lowunit': 'nm', 'up': 800, 'upunit': 'nm', 'B': 3}
        ]
        for item in self.spectrumPresets:
            self.ui.cbPresets.addItem(item['name'])

        gm = [(0, 0, 0), (.15, .15, .5), (.3, .15, .75),
              (.6, .2, .50), (1, .25, .15), (.9, .5, 0),
              (.9, .75, .1), (.9, .9, .5), (1, 1, 1)]
        gerimap = LinearSegmentedColormap.from_list('GeriMap', gm)
        gerimap_r = LinearSegmentedColormap.from_list('GeriMap_r', gm[::-1])
        plt.register_cmap(cmap=gerimap)
        plt.register_cmap(cmap=gerimap_r)

        self.MINTHRESHOLD = -20
        self.threshold = 1e-2

        self.bindEvents()

    def bindEvents(self):
        self.ui.btnBrowse.clicked.connect(self.browseFile)
        self.ui.cbVariable.currentTextChanged.connect(self.variableChanged)
        self.ui.btnLoad.clicked.connect(self.loadFunction)
        self.ui.btnComputeW.clicked.connect(self.showWeighting)
        self.ui.btnShowPlot.clicked.connect(self.showPlots)
        #self.ui.rbPPitch.change.connect(self.setLimitSliders)
        self.ui.rbPparPperp.toggled.connect(self.setLimitSliders)
        self.ui.hsParam1.valueChanged.connect(self.sliderChanged)
        self.ui.hsParam2.valueChanged.connect(self.sliderChanged)
        self.ui.cbPlotParticles.toggled.connect(self.refreshPlots)
        self.ui.cbLogarithmic.toggled.connect(self.refreshPlots)
        self.ui.tbFunction.textChanged.connect(self.enableLoad)
        self.ui.cbTime.currentTextChanged.connect(self.enableLoad)
        #self.ui.rbFullSpectrum.toggled.connect(self.recomputeWeight)
        #self.ui.tbLambda1.textChanged.connect(self.recomputeWeight)
        #self.ui.tbLambda2.textChanged.connect(self.recomputeWeight)
        #self.ui.cbLambda1Unit.currentTextChanged.connect(self.recomputeWeight)
        #self.ui.cbLambda2Unit.currentTextChanged.connect(self.recomputeWeight)
        #self.ui.tbMagField.currentTextChanged.connect(self.recomputeWeight)
        self.ui.btnRecompute.clicked.connect(self.recomputeWeight)
        self.ui.hsThreshold.valueChanged.connect(self.thresholdChanged)
        self.ui.btnOptimize.clicked.connect(self.optimizeGrid)
        self.gridWindow.ui.btnVisualize.clicked.connect(self.visualizeGrid)
        self.ui.btnDominate.clicked.connect(self.findDominant)
        self.ui.btnExport.clicked.connect(self.export)
        self.ui.cbPresets.currentTextChanged.connect(self.presetChanged)

    def browseFile(self):
        filename, _ = QFileDialog.getOpenFileName(parent=self, caption="Open CODE distribution", filter="CODE Distribution (*.mat)")

        if filename:
            self.ui.tbFunction.setText(filename)
            self.matfile = scipy.io.loadmat(filename)
            self.ui.cbVariable.clear()
            
            for var in self.matfile.keys():
                if not var.startswith('__'):
                    self.ui.cbVariable.addItem(var)

    def closeEvent(self, event):
        self.exit()

    def computeWeighting(self):
        self.ui.btnRecompute.setEnabled(False)
        cd = self.codedist

        PARAM1, PARAM2, d = self.getCoordinates()
        F = np.multiply(cd.f, d)
        W = 1

        if self.ui.rbFullSpectrum.isChecked():
            lambda1 = float(self.ui.tbLambda1.text()) * self.wavelengthStringToFloat(self.ui.cbLambda1Unit.currentText())
            lambda2 = float(self.ui.tbLambda2.text()) * self.wavelengthStringToFloat(self.ui.cbLambda2Unit.currentText())

            W = cd.getFullWeighting(lambda1, lambda2, float(self.ui.tbMagField.text()))
        else:
            W = cd.PPERP**2

        F = np.multiply(F, W)
        F = np.divide(F, np.amax(np.amax(F)))

        self.ui.btnRecompute.setEnabled(True)

        return F

    def disableOptions(self):
        self.ui.gbCoordinates.setEnabled(False)
        self.ui.gbSWeighting.setEnabled(False)
        self.ui.cbLogarithmic.setEnabled(False)
        self.ui.btnShowPlot.setEnabled(False)
        self.ui.cbPlotParticles.setEnabled(False)
        self.ui.cbNormalizedUnits.setEnabled(False)
        self.ui.label_6.setEnabled(False)
        self.ui.lblThreshold.setEnabled(False)
        self.ui.hsThreshold.setEnabled(False)
        self.ui.btnExport.setEnabled(False)
        self.ui.btnOptimize.setEnabled(False)

    def enableLoad(self):
        self.ui.btnLoad.setEnabled(True)
        self.disableOptions()

    def enableOptions(self):
        self.ui.gbCoordinates.setEnabled(True)
        self.ui.gbSWeighting.setEnabled(True)
        self.ui.cbLogarithmic.setEnabled(True)
        self.ui.btnShowPlot.setEnabled(True)
        self.ui.cbPlotParticles.setEnabled(True)
        self.ui.cbNormalizedUnits.setEnabled(True)
        self.ui.label_6.setEnabled(True)
        self.ui.lblThreshold.setEnabled(True)
        self.ui.hsThreshold.setEnabled(True)
        self.ui.btnExport.setEnabled(True)
        self.ui.btnOptimize.setEnabled(True)

    def exit(self):
        if self.plotDistWindow.isVisible():
            self.plotDistWindow.close()
        if self.plotWeightWindow.isVisible():
            self.plotWeightWindow.close()

    def export(self):
        if not self.exportWindow.isVisible():
            self.exportWindow.codedist = self.codedist
            self.exportWindow.show()

    def findDominant(self):
        if self.WF is None:
            self.WF = self.computeWeighting()

        PARAM1, PARAM2, d = self.getCoordinates()
        ni, nj = self.WF.shape
        i = np.argmax(self.WF)
        j = i % nj
        i = i // nj

        p1max = PARAM1[i,j]
        p2max = PARAM2[i,j]

        pmax, pitchmax = 0, 0
        if self.ui.rbPPitch.isChecked():
            pmax = p2max
            pitchmax = p1max
        else:
            pmax = np.sqrt(p1max**2 + p2max**2)
            pitchmax = np.arccos(p1max / pmax)

        if self.plotWeightWindow.isVisible():
            self.plotWeightWindow.mark(p1max, p2max)
            
        QMessageBox.information(self, 'Dominant energy and pitch angle', 'p = %.2f MeV/c\npitch = %.3f rad' % (pmax*self.mc, pitchmax))

    def getCoordinates(self):
        cd = self.codedist
        if self.ui.rbPPitch.isChecked():
            return cd.THETA, cd.P, np.multiply(cd.f, np.multiply(cd.P, cd.PPERP))
        else:
            return cd.PPAR, cd.PPERP, np.multiply(cd.f, cd.PPERP)

    def getSliderValues(self):
        perc1 = self.ui.hsParam1.value() * .01
        perc2 = self.ui.hsParam2.value() * .01
        mxparam1 = 1
        mxparam2 = 1

        if self.ui.rbPPitch.isChecked():
            mxparam1 = self.codedist.getParameterMax('pitch')
            mxparam2 = self.codedist.getParameterMax('p')
        else:
            mxparam1 = self.codedist.getParameterMax('ppar')
            mxparam2 = self.codedist.getParameterMax('pperp')

        return (mxparam1*perc1), (mxparam2*perc2)

    def loadFunction(self):
        varname = self.ui.cbVariable.currentText()

        os = self.matfile[varname]
        f = os[0,0]['f']
        y = os[0,0]['y'][0]
        delta = os[0,0]['delta'][0][0]
        Nxi = os[0,0]['Nxi'][0][0]
        #times = os[0,0]['times']

        if self.ui.cbTime.currentText() is 'N/A':
            print('No time slices, or no "times" variable present. Picking last (or only) timestep.')
            f = f[:,f.shape[1]-1]
        else:
            f = f[:,self.ui.cbTime.currentIndex()]

        self.codedist = CodeDistribution(f, y, delta, Nxi)
        self.enableOptions()
        self.setLimitSliders()

        self.ui.btnLoad.setEnabled(False)

    def optimizeGrid(self):
        WF = self.WF
        PARAM1, PARAM2, d = self.getCoordinates()

        if WF is None:
            cd = self.codedist
            WF = np.multiply(cd.f, d)
            W = 1

            if self.ui.rbFullSpectrum.isChecked():
                lambda1 = float(self.ui.tbLambda1.text()) * self.wavelengthStringToFloat(self.ui.cbLambda1Unit.currentText())
                lambda2 = float(self.ui.tbLambda2.text()) * self.wavelengthStringToFloat(self.ui.cbLambda2Unit.currentText())

                W = cd.getFullWeighting(lambda1, lambda2, float(self.ui.tbMagField.text()))
            else:
                W = cd.PPERP**2

            WF = np.multiply(WF, W)
            WF = np.divide(WF, np.amax(np.amax(WF)))
            self.WF = WF

        self.gridWindow.f = WF
        self.gridWindow.X = PARAM1
        self.gridWindow.Y = PARAM2
        self.gridWindow.normalizedUnits = self.ui.cbNormalizedUnits.isChecked()

        if self.ui.rbPPitch.isChecked():
            self.gridWindow.coordinates = 'p'
        else:
            self.gridWindow.coordinates = 'ppar'

        if not self.gridWindow.isVisible():
            self.gridWindow.show()

    def presetChanged(self):
        prs = {}
        for item in self.spectrumPresets:
            if item['name'] == self.ui.cbPresets.currentText():
                prs = item
                break

        self.ui.tbLambda1.setText(str(prs['low']))
        self.ui.tbLambda2.setText(str(prs['up']))
        self.ui.cbLambda1Unit.setCurrentText(prs['lowunit'])
        self.ui.cbLambda2Unit.setCurrentText(prs['upunit'])
        self.ui.tbMagField.setText(str(prs['B']))

    def recomputeWeight(self):
        self.WF = self.computeWeighting()
        if self.plotWeightWindow.isVisible():
            self.showWeighting()

    def refreshPlots(self):
        if self.plotDistWindow.isVisible():
            self.showPlots()
        if self.plotWeightWindow.isVisible():
            self.showWeighting()

    def setLimitSliders(self):
        if self.ui.rbPPitch.isChecked():
            self.ui.lblHsParam1.setText('Maximum pitch angle')
            self.ui.lblHsParam2.setText('Maximum p')
        else:
            self.ui.lblHsParam1.setText('Maximum ppar')
            self.ui.lblHsParam2.setText('Maximum pperp')

        self.sliderChanged()

    def showPlots(self):
        if not self.plotDistWindow.isVisible():
            self.plotDistWindow.show()

        cd = self.codedist

        # Choose coordinates
        PARAM1, PARAM2, d = self.getCoordinates()
        F = np.copy(cd.f)

        # Plot number of particles instead of just f?
        if self.ui.cbPlotParticles.isChecked():
            F = np.multiply(F, d)

        mxpar1, mxpar2 = self.getSliderValues()
        self.plotDistWindow.plot(PARAM1, PARAM2, F, cutoff=self.threshold, logarithmic=self.ui.cbLogarithmic.isChecked(), xmax=mxpar1, ymax=mxpar2)

    def showWeighting(self):
        if not self.plotWeightWindow.isVisible():
            self.plotWeightWindow.show()

        if self.WF is None:
            self.WF = self.computeWeighting()

        PARAM1, PARAM2, d = self.getCoordinates()

        mxpar1, mxpar2 = self.getSliderValues()
        self.plotWeightWindow.plot(PARAM1, PARAM2, self.WF, cutoff=self.threshold, logarithmic=self.ui.cbLogarithmic.isChecked(), xmax=mxpar1, ymax=mxpar2)

    def sliderChanged(self):
        mxpar1, mxpar2 = self.getSliderValues()

        self.ui.lblMaxParam1.setText('%.2f' % (mxpar1))
        self.ui.lblMaxParam2.setText('%.2f' % (mxpar2))

        if self.plotDistWindow.isVisible():
            self.plotDistWindow.setAxisLim(mxpar1, mxpar2)
        if self.plotWeightWindow.isVisible():
            self.plotWeightWindow.setAxisLim(mxpar1, mxpar2)

    def thresholdChanged(self):
        perc = self.ui.hsThreshold.value() * .01
        self.threshold = np.power(10, self.MINTHRESHOLD * perc)
        self.ui.lblThreshold.setText('%.1f' % (self.MINTHRESHOLD*perc))

        if self.plotDistWindow.isVisible():
            self.plotDistWindow.setThreshold(self.threshold)
        if self.plotWeightWindow.isVisible():
            self.plotWeightWindow.setThreshold(self.threshold)

    def variableChanged(self):
        varname = self.ui.cbVariable.currentText()
        os = self.matfile[varname]
        self.ui.cbTime.clear()

        try:
            times = os[0,0]['times'][0]
            if len(times) > 1:
                for t in times:
                    self.ui.cbTime.addItem('%.3f s' % t)
                self.ui.cbTime.setEnabled(True)
            else:
                self.ui.cbTime.addItem('N/A')
                self.ui.cbTime.setEnabled(False)
        except ValueError:
            print('Distribution contains no time-slices')

    def visualizeGrid(self):
        if not self.plotWeightWindow.isVisible(): return

        p1max = self.gridWindow.param1max
        p1min = self.gridWindow.param1min
        p1n   = self.gridWindow.param1n
        p2max = self.gridWindow.param2max
        p2min = self.gridWindow.param2min
        p2n   = self.gridWindow.param2n

        if self.ui.cbNormalizedUnits.isChecked():
            p1max = p1max / self.gridWindow.mc
            p1min = p1min / self.gridWindow.mc
            p2max = p2max / self.gridWindow.mc
            p2min = p2min / self.gridWindow.mc

        self.plotWeightWindow.visualizeGrid(p1min, p1max, p1n, p2min, p2max, p2n)
        
    def wavelengthStringToFloat(self, s):
        if s == 'nm': return 1e-9
        elif s == 'µm': return 1e-6
        elif s == 'pm': return 1e-12
        elif s == 'mm': return 1e-3
        elif s == 'm': return 1
        else:
            raise ValueError('Unrecognized wavelength unit: '+s)

