# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/grid.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Grid(object):
    def setupUi(self, Grid):
        Grid.setObjectName("Grid")
        Grid.resize(510, 240)
        self.buttonBox = QtWidgets.QDialogButtonBox(Grid)
        self.buttonBox.setGeometry(QtCore.QRect(200, 200, 301, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Grid)
        self.label.setGeometry(QtCore.QRect(10, 10, 131, 28))
        self.label.setObjectName("label")
        self.tbPoints = QtWidgets.QLineEdit(Grid)
        self.tbPoints.setGeometry(QtCore.QRect(140, 10, 111, 28))
        self.tbPoints.setObjectName("tbPoints")
        self.btnOptimize = QtWidgets.QPushButton(Grid)
        self.btnOptimize.setGeometry(QtCore.QRect(373, 10, 131, 28))
        self.btnOptimize.setObjectName("btnOptimize")
        self.lblNameParam1 = QtWidgets.QLabel(Grid)
        self.lblNameParam1.setGeometry(QtCore.QRect(10, 80, 31, 20))
        self.lblNameParam1.setObjectName("lblNameParam1")
        self.lblNameParam2 = QtWidgets.QLabel(Grid)
        self.lblNameParam2.setGeometry(QtCore.QRect(10, 100, 63, 20))
        self.lblNameParam2.setObjectName("lblNameParam2")
        self.label_2 = QtWidgets.QLabel(Grid)
        self.label_2.setGeometry(QtCore.QRect(100, 50, 41, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Grid)
        self.label_3.setGeometry(QtCore.QRect(230, 50, 31, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Grid)
        self.label_4.setGeometry(QtCore.QRect(360, 50, 121, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.lblParam1Start = QtWidgets.QLabel(Grid)
        self.lblParam1Start.setGeometry(QtCore.QRect(100, 80, 111, 20))
        self.lblParam1Start.setObjectName("lblParam1Start")
        self.lblParam1End = QtWidgets.QLabel(Grid)
        self.lblParam1End.setGeometry(QtCore.QRect(230, 80, 111, 20))
        self.lblParam1End.setObjectName("lblParam1End")
        self.lblParam1N = QtWidgets.QLabel(Grid)
        self.lblParam1N.setGeometry(QtCore.QRect(360, 80, 63, 20))
        self.lblParam1N.setObjectName("lblParam1N")
        self.lblParam2Start = QtWidgets.QLabel(Grid)
        self.lblParam2Start.setGeometry(QtCore.QRect(100, 100, 111, 20))
        self.lblParam2Start.setObjectName("lblParam2Start")
        self.lblParam2End = QtWidgets.QLabel(Grid)
        self.lblParam2End.setGeometry(QtCore.QRect(230, 100, 111, 20))
        self.lblParam2End.setObjectName("lblParam2End")
        self.lblParam2N = QtWidgets.QLabel(Grid)
        self.lblParam2N.setGeometry(QtCore.QRect(360, 100, 63, 20))
        self.lblParam2N.setObjectName("lblParam2N")
        self.tbSOFT = QtWidgets.QPlainTextEdit(Grid)
        self.tbSOFT.setGeometry(QtCore.QRect(10, 149, 491, 51))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        self.tbSOFT.setFont(font)
        self.tbSOFT.setReadOnly(True)
        self.tbSOFT.setObjectName("tbSOFT")
        self.label_6 = QtWidgets.QLabel(Grid)
        self.label_6.setGeometry(QtCore.QRect(10, 130, 81, 20))
        self.label_6.setObjectName("label_6")
        self.btnVisualize = QtWidgets.QPushButton(Grid)
        self.btnVisualize.setEnabled(False)
        self.btnVisualize.setGeometry(QtCore.QRect(10, 202, 101, 28))
        self.btnVisualize.setObjectName("btnVisualize")

        self.retranslateUi(Grid)
        self.buttonBox.accepted.connect(Grid.accept)
        self.buttonBox.rejected.connect(Grid.reject)
        QtCore.QMetaObject.connectSlotsByName(Grid)

    def retranslateUi(self, Grid):
        _translate = QtCore.QCoreApplication.translate
        Grid.setWindowTitle(_translate("Grid", "Optimize grid"))
        self.label.setText(_translate("Grid", "Number of points:"))
        self.tbPoints.setText(_translate("Grid", "30000"))
        self.btnOptimize.setText(_translate("Grid", "Determine grid"))
        self.lblNameParam1.setText(_translate("Grid", "pitch"))
        self.lblNameParam2.setText(_translate("Grid", "p"))
        self.label_2.setText(_translate("Grid", "Start"))
        self.label_3.setText(_translate("Grid", "End"))
        self.label_4.setText(_translate("Grid", "Number of points"))
        self.lblParam1Start.setText(_translate("Grid", "0"))
        self.lblParam1End.setText(_translate("Grid", "0"))
        self.lblParam1N.setText(_translate("Grid", "∞"))
        self.lblParam2Start.setText(_translate("Grid", "0"))
        self.lblParam2End.setText(_translate("Grid", "0"))
        self.lblParam2N.setText(_translate("Grid", "∞"))
        self.tbSOFT.setPlainText(_translate("Grid", "pitch=0,0,100;\n"
"p=0,0,100;"))
        self.label_6.setText(_translate("Grid", "SOFT code:"))
        self.btnVisualize.setText(_translate("Grid", "Visualize"))

