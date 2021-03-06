import sys
from currency_gui import *
from PyQt5 import QtCore, QtGui, QtWidgets
import urllib3  
import json
urllib3.disable_warnings()

def signals(self):
    self.actionDownload_Rates.triggered.connect(self.download)
    self.lineEdit_1.textEdited['QString'].connect(self.edit1_change)
    self.lineEdit_2.textEdited['QString'].connect(self.edit2_change)
    self.comboBox_1.activated[str].connect(self.edit1_change)
    self.comboBox_2.activated[str].connect(self.edit2_change)
    
def download(self):

    http = urllib3.PoolManager()  
    try:
        r = http.request('GET', 'http://data.fixer.io/api/latest?access_key=396c72203e9a26a6d0cb2ad64bc4e3a6&format=1', retries=False)  # Rates are quoted against the default base (EUR).

        data = r.data.decode('utf-8')
        print(data)
    
        print('Download Successfully!')  # For debugging
        self.actionDownload_Rates.setEnabled(False) 
        r.close()

        data = json.loads(data)
        self.rates = data['rates']
        for key, value in self.rates.items():
            # Manage default base rate: EUR for free fixer account
            baseIndex = self.comboBox_1.findText(data['base'])
            self.comboBox_1.setCurrentIndex(baseIndex)
            self.comboBox_2.setCurrentIndex(baseIndex)

            self.comboBox_1.addItem(key)
            self.comboBox_2.addItem(key)
    except urllib3.exceptions.NewConnectionError:
        QtWidgets.QMessageBox.critical(MainWindow, 'Error', 'Download failed!', QtWidgets.QMessageBox.Ok)

def edit1_change(self):
    key1 = self.comboBox_1.currentText()
    key2 = self.comboBox_2.currentText()
    rate = self.rates[key2]/self.rates[key1]
    amount = float(self.lineEdit_1.text()) * rate
    self.lineEdit_2.setText('{:.2f}'.format(amount))

def edit2_change(self):
    key1 = self.comboBox_1.currentText()
    key2 = self.comboBox_2.currentText()
    rate = self.rates[key1]/self.rates[key2]
    amount = float(self.lineEdit_2.text()) * rate
    self.lineEdit_1.setText('{:.2f}'.format(amount))

Ui_MainWindow.signals = signals
Ui_MainWindow.download = download
Ui_MainWindow.edit1_change = edit1_change
Ui_MainWindow.edit2_change = edit2_change

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.signals()
    MainWindow.show()
    sys.exit(app.exec_())

