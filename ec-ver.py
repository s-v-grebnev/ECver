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
        self.connect(self.ui.pushButton, QtCore.SIGNAL("clicked()"), self.on_clicked_check)
        self.connect(self.ui.actionLoad_Test_256, QtCore.SIGNAL("triggered()"), self.FillTest256)
        self.connect(self.ui.actionLoad_Test_512, QtCore.SIGNAL("triggered()"), self.FillTest512)
        self.connect(self.ui.actionClear_2, QtCore.SIGNAL("triggered()"), self.onClickedClear)
        self.connect(self.ui.actionClear_output, QtCore.SIGNAL("triggered()"), self.onClickedClear_output)
        self.connect(self.ui.actionCheck, QtCore.SIGNAL("triggered()"), self.on_clicked_check)
        self.connect(self.ui.actionQuit,   QtCore.SIGNAL("triggered()"), app.quit)
        self.connect(self.ui.actionOpen,   QtCore.SIGNAL("triggered()"), self.LoadFile)
        self.connect(self.ui.actionSave,   QtCore.SIGNAL("triggered()"), self.SaveFile)
        self.connect(self.ui.action_Run_self_test, QtCore.SIGNAL("triggered()"), self.SelfTest)
        self.connect(self.ui.actionRun_Atkin, QtCore.SIGNAL("triggered()"), self.Atkin)
        self.connect(self.ui.action_Options, QtCore.SIGNAL("triggered()"), self.OptionsDialog)

#    @QtCore.pyqtSlot()

    def FillTest256(self):
        self.ui.lineEdit.setText(str("8000000000000000000000000000000000000000000000000000000000000431"))
        self.ui.lineEdit_2.setText(str("8000000000000000000000000000000150FE8A1892976154C59CFC193ACCF5B3"))
        self.ui.lineEdit_3.setText(str("0000000000000000000000000000000000000000000000000000000000000007"))
        self.ui.lineEdit_4.setText(str("5FBFF498AA938CE739B8E022FBAFEF40563F6E6A3472FC2A514C0CE9DAE23B7E"))
        self.ui.lineEdit_5.setText(str("0000000000000000000000000000000000000000000000000000000000000002"))
        self.ui.lineEdit_6.setText(str("08E2A8A0E65147D4BD6316030E16D19C85C97F0A9CA267122B96ABBCEA7E8FC8"))
        self.ui.lineEdit_7.setText(str("GOSTR34102001-Test"))

    def FillTest512(self):
        self.ui.lineEdit.setText(str("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFDC7"))
        self.ui.lineEdit_2.setText(str("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF27E69532F48D89116FF22B8D4E0560609B4B38ABFAD2B85DCACDB1411F10B275"))
        self.ui.lineEdit_3.setText(str("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFDC4"))
        self.ui.lineEdit_4.setText(str("E8C2505DEDFC86DDC1BD0B2B6667F1DA34B82574761CB0E879BD081CFD0B6265EE3CB090F30D27614CB4574010DA90DD862EF9D4EBEE4761503190785A71C760"))
        self.ui.lineEdit_5.setText(str("00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003"))
        self.ui.lineEdit_6.setText(str("7503CFE87A836AE3A61B8816E25450E6CE5E1C93ACF1ABC1778064FDCBEFA921DF1626BE4FD036E93D75E6A50E3A41E98028FE5FC235F5B889A589CB5215F2A4"))
        self.ui.lineEdit_7.setText(str("GOSTR34102012-Test"))

    def onClickedClear_output(self):
        self.ui.plainTextEdit.clear()

    def onClickedClear(self):
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


    def on_clicked_check(self):
        params = []
        log = []
        flag = False
        number = str(int(str(self.ui.lineEdit.text()), base = 16))
        try:
            params.append(str(self.ui.lineEdit.text()))
            params.append(str(self.ui.lineEdit_2.text()))
            params.append(str(self.ui.lineEdit_3.text()))
            params.append(str(self.ui.lineEdit_4.text()))
            params.append(str(self.ui.lineEdit_5.text()))
            params.append(str(self.ui.lineEdit_6.text()))
            EC = ec.elliptic_curve(str(self.ui.lineEdit_7.text()), params, 16)
            flag, log = EC.gosttest(opts.GetOption('OutputBase'))
        except(TypeError) as err:
            QtGui.QMessageBox.critical(self, "Invalid input", err.args[0])
            self.ui.plainTextEdit.insertPlainText("Invalid input; please check\n")
        except(ValueError) as err:
            QtGui.QMessageBox.critical(self, "Invalid input", err.args[0] )
            self.ui.plainTextEdit.insertPlainText("Invalid input; please check\n")

        for i in log:
            self.ui.plainTextEdit.insertPlainText(i + '\n')
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
        import subprocess as sp
        AtkinPath=''
        if opts.GetOption('AtkinPath') == '':
            AtkinPath = QtGui.QFileDialog.getOpenFileName(caption = "Path to Atkin")
        else:
            AtkinPath = opts.GetOption('AtkinPath')
#        print(AtkinPath)
        with sp.Popen([AtkinPath], stdin = sp.PIPE) as fp:
#                fp.communicate(str(int(self.ui.lineEdit.text(), base = 16))+'\n')
            text = self.ui.lineEdit.text()
            text = format('%s' % text)
            text = str(int(text, base = 16))+'\n'
            fp.communicate(bytes(text, 'UTF-8'))
            p_res = fp.returncode
        with sp.Popen([AtkinPath], stdin = sp.PIPE) as fp:
            text = self.ui.lineEdit_2.text()
            text = format('%s' % text)
            text = str(int(text, base = 16))+'\n'
            fp.communicate(bytes(text, 'UTF-8'))
            q_res = fp.returncode

        if p_res == 0 and q_res == 0:
            QtGui.QMessageBox.information(self, "Atkin says!", "Atkin said: P, Q are proven primes")
        elif p_res == 2 or q_res == 2:
            QtGui.QMessageBox.critical(self, "Atkin says!", "Atkin said: P or Q is composite")
        else:
            QtGui.QMessageBox.information(self, "Atkin says!", "Atkin said: P ,Q are probably prime")


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
        QtCore.QObject.connect(dialog.toolButton,  QtCore.SIGNAL("clicked()"), dialog.GetAtkinName)
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

