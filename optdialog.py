# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'optdialog.ui'
#
# Created: Thu Sep  7 18:23:00 2017
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Options(QtWidgets.QDialog):
    def setupUi(self, Options):
        Options.setObjectName(_fromUtf8("Options"))
        Options.resize(548, 192)
        self.buttonBox = QtWidgets.QDialogButtonBox(Options)
        self.buttonBox.setGeometry(QtCore.QRect(190, 140, 341, 32))
        self.buttonBox.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.checkBox = QtWidgets.QCheckBox(Options)
        self.checkBox.setGeometry(QtCore.QRect(20, 40, 78, 20))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.horizontalSlider = QtWidgets.QSlider(Options)
        self.horizontalSlider.setGeometry(QtCore.QRect(170, 20, 160, 16))
        self.horizontalSlider.setMinimum(100)
        self.horizontalSlider.setMaximum(256)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName(_fromUtf8("horizontalSlider"))
        self.label = QtWidgets.QLabel(Options)
        self.label.setGeometry(QtCore.QRect(20, 20, 171, 16))
        self.label.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.label.setObjectName(_fromUtf8("label"))
        self.lineEdit = QtWidgets.QLineEdit(Options)
        self.lineEdit.setGeometry(QtCore.QRect(120, 70, 391, 22))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.toolButton = QtWidgets.QToolButton(Options)
        self.toolButton.setGeometry(QtCore.QRect(520, 70, 24, 21))
        self.toolButton.setObjectName(_fromUtf8("toolButton"))
        self.label_4 = QtWidgets.QLabel(Options)
        self.label_4.setGeometry(QtCore.QRect(20, 70, 111, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.frame = QtWidgets.QFrame(Options)
        self.frame.setGeometry(QtCore.QRect(10, 100, 151, 71))
        self.frame.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 31, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.radioButton_2 = QtWidgets.QRadioButton(self.frame)
        self.radioButton_2.setGeometry(QtCore.QRect(50, 10, 92, 20))
        self.radioButton_2.setChecked(True)
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.radioButton = QtWidgets.QRadioButton(self.frame)
        self.radioButton.setGeometry(QtCore.QRect(50, 40, 92, 21))
        self.radioButton.setObjectName(_fromUtf8("radioButton"))

        self.retranslateUi(Options)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Options.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Options.accept)
        QtCore.QMetaObject.connectSlotsByName(Options)

    def retranslateUi(self, Options):
        Options.setWindowTitle(_translate("Options", "Options", None))
        self.checkBox.setText(_translate("Options", "Use Atkin", None))
        self.label.setText(_translate("Options", "Miller-Rabin iterations", None))
        self.toolButton.setText(_translate("Options", "...", None))
        self.label_4.setText(_translate("Options", "Atkin executable:", None))
        self.label_2.setText(_translate("Options", "Base:", None))
        self.radioButton_2.setText(_translate("Options", "16", None))
        self.radioButton.setText(_translate("Options", "10", None))

