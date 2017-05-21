# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/output.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Output(object):
    def setupUi(self, Output):
        Output.setObjectName("Output")
        Output.resize(480, 308)
        self.buttonBox = QtWidgets.QDialogButtonBox(Output)
        self.buttonBox.setGeometry(QtCore.QRect(10, 270, 461, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.rbRadialFile = QtWidgets.QRadioButton(Output)
        self.rbRadialFile.setGeometry(QtCore.QRect(10, 10, 371, 26))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.rbRadialFile.setFont(font)
        self.rbRadialFile.setObjectName("rbRadialFile")
        self.gbUniform = QtWidgets.QGroupBox(Output)
        self.gbUniform.setGeometry(QtCore.QRect(10, 100, 461, 71))
        self.gbUniform.setTitle("")
        self.gbUniform.setObjectName("gbUniform")
        self.label = QtWidgets.QLabel(self.gbUniform)
        self.label.setGeometry(QtCore.QRect(10, 30, 61, 28))
        self.label.setObjectName("label")
        self.tbRad1 = QtWidgets.QLineEdit(self.gbUniform)
        self.tbRad1.setGeometry(QtCore.QRect(80, 30, 51, 28))
        self.tbRad1.setObjectName("tbRad1")
        self.label_2 = QtWidgets.QLabel(self.gbUniform)
        self.label_2.setGeometry(QtCore.QRect(140, 30, 61, 28))
        self.label_2.setObjectName("label_2")
        self.tbRad2 = QtWidgets.QLineEdit(self.gbUniform)
        self.tbRad2.setGeometry(QtCore.QRect(210, 30, 51, 28))
        self.tbRad2.setObjectName("tbRad2")
        self.label_3 = QtWidgets.QLabel(self.gbUniform)
        self.label_3.setGeometry(QtCore.QRect(270, 30, 63, 28))
        self.label_3.setObjectName("label_3")
        self.tbRadialFile = QtWidgets.QLineEdit(Output)
        self.tbRadialFile.setEnabled(False)
        self.tbRadialFile.setGeometry(QtCore.QRect(10, 40, 371, 28))
        self.tbRadialFile.setObjectName("tbRadialFile")
        self.btnBrowse = QtWidgets.QPushButton(Output)
        self.btnBrowse.setEnabled(False)
        self.btnBrowse.setGeometry(QtCore.QRect(390, 40, 81, 28))
        self.btnBrowse.setObjectName("btnBrowse")
        self.rbGenerateProfile = QtWidgets.QRadioButton(Output)
        self.rbGenerateProfile.setGeometry(QtCore.QRect(10, 90, 181, 26))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.rbGenerateProfile.setFont(font)
        self.rbGenerateProfile.setChecked(True)
        self.rbGenerateProfile.setObjectName("rbGenerateProfile")
        self.btnGenerate = QtWidgets.QPushButton(Output)
        self.btnGenerate.setGeometry(QtCore.QRect(10, 272, 84, 28))
        self.btnGenerate.setObjectName("btnGenerate")

        self.retranslateUi(Output)
        self.buttonBox.accepted.connect(Output.accept)
        self.buttonBox.rejected.connect(Output.reject)
        QtCore.QMetaObject.connectSlotsByName(Output)

    def retranslateUi(self, Output):
        _translate = QtCore.QCoreApplication.translate
        Output.setWindowTitle(_translate("Output", "Generate SOFT distribution"))
        self.rbRadialFile.setText(_translate("Output", "Radial profile from file"))
        self.label.setText(_translate("Output", "From r ="))
        self.tbRad1.setText(_translate("Output", "0.5"))
        self.label_2.setText(_translate("Output", "m to r ="))
        self.tbRad2.setText(_translate("Output", "1.5"))
        self.label_3.setText(_translate("Output", "m"))
        self.btnBrowse.setText(_translate("Output", "Browse..."))
        self.rbGenerateProfile.setText(_translate("Output", "Uniform radial profile"))
        self.btnGenerate.setText(_translate("Output", "Generate"))

