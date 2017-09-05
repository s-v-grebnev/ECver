import math
import random
import time

import ec
import primeq

T = ec.elliptic_curve('Fuck', ['0', '0', '0', '0', '0', '0'], 16)
try:
    T.selftest()
except ec.TestError as err:
    print('Self-test failed: ' + err.msg)
else:
    print('Self-test OK')

EC = ec.elliptic_curve("Test", ["8000000000000000000000000000000000000000000000000000000000000431",
                    "8000000000000000000000000000000150FE8A1892976154C59CFC193ACCF5B3",
                    "0000000000000000000000000000000000000000000000000000000000000007",
                    "5FBFF498AA938CE739B8E022FBAFEF40563F6E6A3472FC2A514C0CE9DAE23B7E",
                    "0000000000000000000000000000000000000000000000000000000000000002",
                    "08E2A8A0E65147D4BD6316030E16D19C85C97F0A9CA267122B96ABBCEA7E8FC8"],
                    16)

#skey = 55441196065363246126355624130324183196576709222340016572108097750006097525544L
#Q = EC.mul(skey, EC.P)
#print 'Public key =', Q
# Q = 57520216126176808443631405...

#digest = 20798893674476452017134061561508270130637142515379653289952617252661468872421L
#rnd = 53854137677348463731403841147996619241504003434302020712960838528893196233395L

#print 'R = ', EC.mul(rnd, EC.P)
# R = 29700980915817952874371...

#signature = EC.sign(digest, rnd, skey)
#print 'Signature =',  signature
#print 'Verification:', EC.verify(digest, signature, Q)

#from primeq import primeq
#print primeq(2 ** 521 - 1)


from PyQt4 import QtCore, QtGui
import sys
import mainwindow

class MyWindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.connect(self.ui.pushButton, QtCore.SIGNAL("clicked()"), self.on_clicked_check)
        self.connect(self.ui.actionLoad_Test_256, QtCore.SIGNAL("triggered()"), self.on_clicked_test256)
        self.connect(self.ui.actionLoad_Test_512, QtCore.SIGNAL("triggered()"), self.on_clicked_test512)
        self.connect(self.ui.actionClear_2, QtCore.SIGNAL("triggered()"), self.on_clicked_clear)
        self.connect(self.ui.actionCheck, QtCore.SIGNAL("triggered()"), self.on_clicked_check)
        self.connect(self.ui.actionQuit,   QtCore.SIGNAL("triggered()"), app.quit)
        self.connect(self.ui.actionOpen,   QtCore.SIGNAL("triggered()"), self.LoadFile)
        self.connect(self.ui.actionSave,   QtCore.SIGNAL("triggered()"), self.SaveFile)

#    @QtCore.pyqtSlot()

    def on_clicked_test256(self):
        self.ui.lineEdit.setText(str("8000000000000000000000000000000000000000000000000000000000000431"))
        self.ui.lineEdit_2.setText(str("8000000000000000000000000000000150FE8A1892976154C59CFC193ACCF5B3"))
        self.ui.lineEdit_3.setText(str("0000000000000000000000000000000000000000000000000000000000000007"))
        self.ui.lineEdit_4.setText(str("5FBFF498AA938CE739B8E022FBAFEF40563F6E6A3472FC2A514C0CE9DAE23B7E"))
        self.ui.lineEdit_5.setText(str("0000000000000000000000000000000000000000000000000000000000000002"))
        self.ui.lineEdit_6.setText(str("08E2A8A0E65147D4BD6316030E16D19C85C97F0A9CA267122B96ABBCEA7E8FC8"))

    def on_clicked_test512(self):
        self.ui.lineEdit.setText(str("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFDC7"))
        self.ui.lineEdit_2.setText(str("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF27E69532F48D89116FF22B8D4E0560609B4B38ABFAD2B85DCACDB1411F10B275"))
        self.ui.lineEdit_3.setText(str("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFDC4"))
        self.ui.lineEdit_4.setText(str("E8C2505DEDFC86DDC1BD0B2B6667F1DA34B82574761CB0E879BD081CFD0B6265EE3CB090F30D27614CB4574010DA90DD862EF9D4EBEE4761503190785A71C760"))
        self.ui.lineEdit_5.setText(str("00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003"))
        self.ui.lineEdit_6.setText(str("7503CFE87A836AE3A61B8816E25450E6CE5E1C93ACF1ABC1778064FDCBEFA921DF1626BE4FD036E93D75E6A50E3A41E98028FE5FC235F5B889A589CB5215F2A4"))

    def on_clicked_clear(self):
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()
        self.ui.lineEdit_4.clear()
        self.ui.lineEdit_5.clear()
        self.ui.lineEdit_6.clear()
        self.ui.plainTextEdit.clear()

    def LoadFile(self):
        EC = ec.elliptic_curve()
        f = QtGui.QFileDialog.getOpenFileName()
        EC.loadfromfile(f)
        self.sync_ec(EC)
        self.ui.plainTextEdit.clear()
        
    def SaveFile(self):
        f = QtGui.QFileDialog.getSaveFileNameAndFilter(filter = 'All (*);;Text (*.txt)', initialFilter = 'Text (*.txt)')
        with open(f[0], 'w') as fh:
            fh.write('P=' + str(self.ui.lineEdit.text())+'\n')
            fh.write('Q=' + str(self.ui.lineEdit_2.text())+'\n')
            fh.write('A=' + str(self.ui.lineEdit_3.text())+'\n')
            fh.write('B=' + str(self.ui.lineEdit_4.text())+'\n')
            fh.write('X=' + str(self.ui.lineEdit_5.text())+'\n')
            fh.write('Y=' + str(self.ui.lineEdit_6.text())+'\n')
            fh.write(self.ui.plainTextEdit.toPlainText())


    def on_clicked_check(self):
        params = []
        log = []
#        self.on_clicked_tv()
        try:
            params.append(str(self.ui.lineEdit.text()))
            params.append(str(self.ui.lineEdit_2.text()))
            params.append(str(self.ui.lineEdit_3.text()))
            params.append(str(self.ui.lineEdit_4.text()))
            params.append(str(self.ui.lineEdit_5.text()))
            params.append(str(self.ui.lineEdit_6.text()))
            EC = ec.elliptic_curve("Test", params, 16)
            log = EC.gosttest()
  #      except(TypeError):
   #         self.ui.plainTextEdit.insertPlainText("Invalid input; please check\n")
        except(ValueError):
            self.ui.plainTextEdit.insertPlainText("Invalid input; please check\n")

        for i in log:
            self.ui.plainTextEdit.insertPlainText(i + '\n')
#        sys.exit(app.exec_())

    def sync_ec(self, EC):
        params = EC.getparams()
        self.ui.lineEdit.setText(hex(params[0]).lstrip('0x').rstrip('L'))
        self.ui.lineEdit_2.setText(hex(params[1]).lstrip('0x').rstrip('L'))
        self.ui.lineEdit_3.setText(hex(params[2]).lstrip('0x').rstrip('L'))
        self.ui.lineEdit_4.setText(hex(params[3]).lstrip('0x').rstrip('L'))
        self.ui.lineEdit_5.setText(hex(params[4][0]).lstrip('0x').rstrip('L'))
        self.ui.lineEdit_6.setText(hex(params[4][1]).lstrip('0x').rstrip('L'))

if __name__ == "__main__":
#    EC = ec.elliptic_curve
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

