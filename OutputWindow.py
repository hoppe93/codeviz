
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from ui import output_design
import numpy as np
import os
import hdf5storage

class OutputWindow(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)

        self.ui = output_design.Ui_Output()
        self.ui.setupUi(self)

        self.codedist = None

        self.bindEvents()

    def bindEvents(self):
        self.ui.rbRadialFile.toggled.connect(self.chooseRadialProfile)
        self.ui.btnBrowse.clicked.connect(self.browseFile)
        self.ui.btnGenerate.clicked.connect(self.generate)

    def browseFile(self):
        filename, _ = QFileDialog.getOpenFileName(parent=self, caption='Open radial distribution', filter='Comma/Tab-separated values (*.csv *.dat *.tsv)')

        if filename:
            self.ui.tbRadialFile.setText(filename)

            # Load radial profile
            DATA = np.genfromtxt(filename, delimiter='')
            self.r = DATA[:,0]
            self.profile = DATA[:,1]

    def chooseRadialProfile(self):
        if self.ui.rbRadialFile.isChecked():
            self.ui.gbUniform.setEnabled(False)
            self.ui.tbRadialFile.setEnabled(True)
            self.ui.btnBrowse.setEnabled(True)
        else:
            self.ui.gbUniform.setEnabled(True)
            self.ui.tbRadialFile.setEnabled(False)
            self.ui.btnBrowse.setEnabled(False)

    def generate(self):
        if self.codedist is None:
            raise ValueError('No CODE distribution provided')

        r, profile = [], []

        if self.ui.rbRadialFile.isChecked():
            r = self.r
            profile = self.profile
        else:
            try:
                r1 = float(self.ui.tbRad1.text())
                r2 = float(self.ui.tbRad2.text())

                r = np.array([r1, r2])
                profile = np.array([1.0,1.0])
            except ValueError:
                QMessageBox.error(self, 'Invalid radius', 'The radial interval must be specified as floating point numbers.')
                return

        # Let user decide where to save file
        filename, _ = QFileDialog.getSaveFileName(parent=self, caption='Save SOFT distribution function', filter='SOFT distribution function (*.mat)')
        veldim = len(self.codedist.xis)*len(self.codedist.p)
        fvel = np.reshape(self.codedist.f, (1, veldim))
        F = np.zeros((len(r), veldim))

        for i in range(0,len(r)):
            F[i,:] = fvel * r[i]

        if filename:
            matcontent = {
                u'r': r,
                u'xi': self.codedist.xis,
                u'p': self.codedist.p,
                u'punits': 'normalized',
                u'f': F
            }

            hdf5storage.write(matcontent, '.', filename, store_python_metadata=False, matlab_compatible=True)

            statinfo = os.stat(filename)
            filesize = statinfo.st_size
            suffices = ['B', 'kB', 'MB', 'GB', 'TB']

            i = 0
            while filesize > 1000 and i < len(suffices)-1:
                filesize = filesize / 1000
                i = i + 1

            QMessageBox.information(self, 'Writing done', 'Generated a %.2f%s SOFT distribution function' % (filesize, suffices[i]))
            self.close()

        """
        mc = 9.10938356e-31 * 299792458

        if filename:
            with open(filename, 'w') as f:
                # Print bounds
                f.write('%.12f %.12f %d\n' % (np.amin(r), np.amax(r), len(r)))
                f.write('%.12f %.12f %d\n' % (np.amin(self.codedist.xis), np.amax(self.codedist.xis), len(self.codedist.xis)))
                f.write('%.12f %.12f %d\n' % (np.amin(self.codedist.p*mc), np.amax(self.codedist.p*mc), len(self.codedist.p)))

            with open(filename, 'ab') as f:
                # Print arrays
                np.savetxt(f, r, newline=" ")
                np.savetxt(f, self.codedist.xis, newline=" ")
                np.savetxt(f, self.codedist.p*mc, newline=" ")

                for i in range(0,len(r)):
                    F = self.codedist.f * r[i]
                    np.savetxt(f, F)

            statinfo = os.stat(filename)
            filesize = statinfo.st_size
            suffices = ['B', 'kB', 'MB', 'GB', 'TB']

            i = 0
            while filesize > 1000 and i < len(suffices)-1:
                filesize = filesize / 1000
                i = i + 1

            QMessageBox.information(self, 'Writing done', 'Generated a %.2f%s SOFT distribution function' % (filesize, suffices[i]))
            self.close()
        """
            
