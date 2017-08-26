from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib
import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class PlotWindow(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(PlotWindow, self).__init__(parent)

        self.figure = Figure(facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.image = None
        self.ax = None
        self.captions = list()

        self.f = None
        self.X = None
        self.Y = None
        self.logarithmic = None
        self.xmax = None
        self.ymax = None

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def drawSafe(self):
        try:
            self.canvas.draw()
        except RuntimeError as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(e.strerror)
            msg.setWindowTitle('Runtime Error')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def genPlot(self, fig, X, Y, f, logarithmic=False, cutoff=1e-2,xmax=None,ymax=None):
        """ Generate a contour plot of a CODE distribution function
            f: CodeDistribution function
            coordinates: 1 = ppar / pperp, 2 = p / pitch
        """
        gerimap = plt.get_cmap('GeriMap')
        fig.clf()
        ax = fig.add_subplot(111)

        vmin = cutoff
        vmax = 1

        if logarithmic:
            f[f < vmin] = vmin*1e-1
            vmin = np.log10(vmin)
            vmax = np.log10(vmax)
            f = np.log10(f)

        levels = np.linspace(vmin, vmax, 20)

        cp = ax.contourf(X, Y, f, cmap=gerimap, vmin=vmin, vmax=vmax, levels=levels, antialiased=True)
        cbar = fig.colorbar(cp, shrink=0.8)

        ax.set_facecolor('black')

        if xmax != None:
            ax.set_xlim([0,xmax])
        if ymax != None:
            ax.set_ylim([0,ymax])

        return ax, cp, cbar

    def mark(self, x, y):
        self.ax.plot(x, y, 'rx')
        self.drawSafe()

    def plot(self, X, Y, f, logarithmic=False, cutoff=1e-2, xmax=None, ymax=None):
        self.f = f
        self.X = X
        self.Y = Y
        self.logarithmic = logarithmic
        self.xmax = xmax
        self.ymax = ymax

        self.ax, self.cp, self.cbar = self.genPlot(self.figure, X, Y, f, logarithmic, cutoff, xmax, ymax)

        self.drawSafe()

    def setAxisLim(self, maxx, maxy):
        if self.ax is None: return

        self.ax.set_xlim([0,maxx])
        self.ax.set_ylim([0,maxy])
        self.drawSafe()

    def setThreshold(self, threshold):
        if self.f is None: return

        self.plot(self.X, self.Y, self.f, logarithmic=self.logarithmic, cutoff=threshold, xmax=self.xmax, ymax=self.ymax)

    def visualizeGrid(self, p1min, p1max, p1n, p2min, p2max, p2n):
        p1, p2 = np.meshgrid(np.linspace(p1min, p1max, p1n), np.linspace(p2min, p2max, p2n))
        self.ax.plot(p1, p2, 'r.')
        self.drawSafe()

