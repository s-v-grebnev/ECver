#!/usr/bin/python3
""" GOST R 34.10-20** verification

This program implements verification of GOST R 34.10-2012 digital signature
scheme parameters, that is, elliptic curves
"""

from ecver import ec as ec
from PyQt4 import QtCore, QtGui
import sys
import mainwindow
import options, optdialog
import os
from ecver import atkin_pro, curves

if __name__ == "__main__":
    opts = options.Options()

class SuperUi_Options(optdialog.Ui_Options):
    def GetAtkinName(self):
        f = QtGui.QFileDialog.getOpenFileName()
        if not f == '':
            opts.SetOption("AtkinPath", f)
            self.lineEdit.setText(f)

class MyWindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.CheckEC)
        self.ui.actionLoad_Test_256.triggered.connect(self.FillTest256)
        self.ui.actionLoad_Test_512.triggered.connect(self.FillTest512)
        self.ui.actionClear_2.triggered.connect(self.ClickedClear)
        self.ui.actionClear_output.triggered.connect(self.ClickedClearOutput)
        self.ui.actionCheck.triggered.connect(self.CheckEC)
        self.ui.actionQuit.triggered.connect(app.quit)
        self.ui.actionOpen.triggered.connect(self.LoadFile)
        self.ui.actionSave.triggered.connect(self.SaveFile)
        self.ui.action_Run_self_test.triggered.connect(self.SelfTest)
        self.ui.actionRun_Atkin.triggered.connect(self.Atkin)
        self.ui.action_Options.triggered.connect(self.OptionsDialog)
        self.ui.checkBox.stateChanged.connect(self.SetInputBase)
        self.ui.checkBox.stateChanged.connect(self.SetInputBase)
        self.ui.plainTextEdit.setReadOnly(True)
        self.statusBar().showMessage('Ready')

        #        self.connect(self.ui.pushButton, QtCore.SIGNAL("clicked()"), self.CheckEC)
#        self.connect(self.ui.actionLoad_Test_256, QtCore.SIGNAL("triggered()"), self.FillTest256)
#        self.connect(self.ui.actionLoad_Test_512, QtCore.SIGNAL("triggered()"), self.FillTest512)
#        self.connect(self.ui.actionClear_2, QtCore.SIGNAL("triggered()"), self.ClickedClear)
#        self.connect(self.ui.actionClear_output, QtCore.SIGNAL("triggered()"), self.ClickedClearOutput)
#        self.connect(self.ui.actionCheck, QtCore.SIGNAL("triggered()"), self.CheckEC)
#        self.connect(self.ui.actionQuit,   QtCore.SIGNAL("triggered()"), app.quit)
#        self.connect(self.ui.actionOpen,   QtCore.SIGNAL("triggered()"), self.LoadFile)
#        self.connect(self.ui.actionSave,   QtCore.SIGNAL("triggered()"), self.SaveFile)
#        self.connect(self.ui.action_Run_self_test, QtCore.SIGNAL("triggered()"), self.SelfTest)
#        self.connect(self.ui.actionRun_Atkin, QtCore.SIGNAL("triggered()"), self.Atkin)
#        self.connect(self.ui.action_Options, QtCore.SIGNAL("triggered()"), self.OptionsDialog)
#        self.connect(self.ui.checkBox, QtCore.SIGNAL("stateChanged()"), self.SetInputBase)
### XXX!
        self.ui.checkBox.stateChanged.connect(self.SetInputBase)

#    @QtCore.pyqtSlot()

    def FillTest256(self):
        self.ui.lineEdit.setText(str(curves.Curves['GOSTR34102001-Test']['P']))
        self.ui.lineEdit_2.setText(str(curves.Curves['GOSTR34102001-Test']['Q']))
        self.ui.lineEdit_3.setText(str(curves.Curves['GOSTR34102001-Test']['A']))
        self.ui.lineEdit_4.setText(str(curves.Curves['GOSTR34102001-Test']['B']))
        self.ui.lineEdit_5.setText(str(curves.Curves['GOSTR34102001-Test']['X']))
        self.ui.lineEdit_6.setText(str(curves.Curves['GOSTR34102001-Test']['Y']))
        self.ui.lineEdit_7.setText(str("GOSTR34102001-Test"))

    def FillTest512(self):
        self.ui.lineEdit.setText(str(curves.Curves['GOSTR34102012-Test']['P']))
        self.ui.lineEdit_2.setText(str(curves.Curves['GOSTR34102012-Test']['Q']))
        self.ui.lineEdit_3.setText(str(curves.Curves['GOSTR34102012-Test']['A']))
        self.ui.lineEdit_4.setText(str(curves.Curves['GOSTR34102012-Test']['B']))
        self.ui.lineEdit_5.setText(str(curves.Curves['GOSTR34102012-Test']['X']))
        self.ui.lineEdit_6.setText(str(curves.Curves['GOSTR34102012-Test']['Y']))      
        self.ui.lineEdit_7.setText(str("GOSTR34102012-Test"))

    def ClickedClearOutput(self):
        self.ui.plainTextEdit.clear()

    def ClickedClear(self):
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()
        self.ui.lineEdit_4.clear()
        self.ui.lineEdit_5.clear()
        self.ui.lineEdit_6.clear()

    def SelfTest(self):
        EC = ec.elliptic_curve()
        answer = EC.selftest()
        if answer == True:
            QtGui.QMessageBox.information(self, "Self-test passed", "Self-test passed")
        else:
            QtGui.QMessageBox.critical(self, "Self-test failed", "Self-test failed")

    def LoadFile(self):
        EC = ec.elliptic_curve()
        f = QtGui.QFileDialog.getOpenFileName()
        EC.loadfromfile(f)
        self.sync_ec(EC)
        self.ui.plainTextEdit.clear()
        
    def SaveFile(self):
        f = QtGui.QFileDialog.getSaveFileNameAndFilter(filter = 'All (*);;Text (*.txt)', initialFilter = 'Text (*.txt)')
        try:
            with open(f[0], 'w') as fh:
                fh.write('P=' + str(self.ui.lineEdit.text())+'\n')
                fh.write('Q=' + str(self.ui.lineEdit_2.text())+'\n')
                fh.write('A=' + str(self.ui.lineEdit_3.text())+'\n')
                fh.write('B=' + str(self.ui.lineEdit_4.text())+'\n')
                fh.write('X=' + str(self.ui.lineEdit_5.text())+'\n')
                fh.write('Y=' + str(self.ui.lineEdit_6.text())+'\n')
                fh.write(self.ui.plainTextEdit.toPlainText())
        except:
            QtGui.QMessageBox.critical(self, "Error writing to file", "Error writing to file")

    def CheckEC(self):
        params = []
        log = []
        flag = False
      #  number = str(int(str(self.ui.lineEdit.text()), base = 16))
        try:
            params.append(str(self.ui.lineEdit.text()))
            params.append(str(self.ui.lineEdit_2.text()))
            params.append(str(self.ui.lineEdit_3.text()))
            params.append(str(self.ui.lineEdit_4.text()))
            params.append(str(self.ui.lineEdit_5.text()))
            params.append(str(self.ui.lineEdit_6.text()))
            EC = ec.elliptic_curve(str(self.ui.lineEdit_7.text()), params, int(opts.GetOption('InputBase')))
            flag, log = EC.gosttest(opts.GetOption('OutputBase'))
        except(TypeError, ValueError) as err:
            QtGui.QMessageBox.critical(self, "Invalid input", err.args[0])
            self.ui.plainTextEdit.setReadOnly(False)
            self.ui.plainTextEdit.appendPlainText("Invalid input; please check")
            self.ui.plainTextEdit.setReadOnly(True)
        self.ui.plainTextEdit.setReadOnly(False)
        for i in log:
            self.ui.plainTextEdit.appendPlainText(i)
            self.ui.plainTextEdit.setReadOnly(True)
#        print(flag)
        if flag == True:
            QtGui.QMessageBox.information(self, "Curve satisfies GOST R 34.10", "Curve satisfies GOST R 34.10")


    def sync_ec(self, EC):
        params = EC.getparams()
        self.ui.lineEdit.setText(hex(params[0]).lstrip('0x').rstrip('L'))
        self.ui.lineEdit_2.setText(hex(params[1]).lstrip('0x').rstrip('L'))
        self.ui.lineEdit_3.setText(hex(params[2]).lstrip('0x').rstrip('L'))
        self.ui.lineEdit_4.setText(hex(params[3]).lstrip('0x').rstrip('L'))
        self.ui.lineEdit_5.setText(hex(params[4][0]).lstrip('0x').rstrip('L'))
        self.ui.lineEdit_6.setText(hex(params[4][1]).lstrip('0x').rstrip('L'))

    def Atkin(self):
        AtkinPath=''
        self.statusBar().showMessage('Running ECPP test')
        if opts.GetOption('AtkinPath') == '':
            AtkinPath = QtGui.QFileDialog.getOpenFileName(caption = "Path to Atkin")
        else:
            AtkinPath = opts.GetOption('AtkinPath')

        p_res, q_res = atkin_pro.AtkinTest(self.ui.lineEdit.text(), self.ui.lineEdit_2.text(), AtkinPath)
        if p_res == 0 and q_res == 0:
            QtGui.QMessageBox.information(self, "Atkin says!", "Atkin said: P, Q are proven primes")
        elif p_res == 2 or q_res == 2:
            QtGui.QMessageBox.critical(self, "Atkin says!", "Atkin said: P or Q is composite")
        else:
            QtGui.QMessageBox.information(self, "Atkin says!", "Atkin said: P ,Q are probably prime")
        self.statusBar().showMessage('ECPP test complete' )

    def OptionsDialog(self):
#        import optdialog
#        ecoptions = options.Options()
        dialog = SuperUi_Options()

        dialog.setupUi(dialog)
        if(opts.GetOption('UseAtkin') == 'True'):
            dialog.checkBox.setChecked(True)
        dialog.lineEdit.setText(opts.GetOption('AtkinPath'))
        dialog.horizontalSlider.setValue(int(opts.GetOption('MRIterations')))
        if opts.GetOption('OutputBase') == '16':
            dialog.radioButton_2.setChecked(True)
        #    dialog.radioButton.setChecked(False)
        else:
            dialog.radioButton.setChecked(True)
        #    dialog.radioButton_2.setChecked(False)
        dialog.toolButton.clicked.connect( dialog.GetAtkinName)
        result = dialog.exec_()
        if result == QtGui.QDialog.Accepted:
            if dialog.checkBox.isChecked() == True:
                opts.SetOption('UseAtkin', 'True')
            if dialog.radioButton_2.isChecked() == True:
                opts.SetOption('OutputBase', 16)
            else:
                opts.SetOption('OutputBase', 10)
            opts.SetOption('AtkinPath', dialog.lineEdit.text())
            opts.SetOption('MRIterations', dialog.horizontalSlider.value())
            try:
                opts.SaveOptions(os.getcwd() + '/ec-ver.rc')
            except:
                print('Failed to save options')

    def SetInputBase(self):
        if self.ui.checkBox.isChecked():
            opts.SetOption('InputBase', 16)
        else:
            opts.SetOption('InputBase', 10)


if __name__ == "__main__":
#    EC = ec.elliptic_curve
    try:
        opts.LoadOptions(os.getcwd() + '/ec-ver.rc')
    except:
        print('Failed to load options')
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    window.setWindowIcon(QtGui.QIcon('ec-ver.png'))
    app.setWindowIcon(QtGui.QIcon('ec-ver.png'))
    window.show()
    sys.exit(app.exec_())

