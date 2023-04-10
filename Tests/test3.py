import sys
import progress as progress
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication

import test3_1


class MainUiClass(QtGui.QMainWindow, progress.UI_MainWindow):
    def __init__(self, parent=None):
        super(MainUiClass, self).__init__(parent)
        self.setupUi(self)
        self.threadclass = ThreadClass()
        self.threadclass.start()
        self.connect(self.threadclass, QtCore.SIGNAL('CPU_VALUE'), self.updateProgressBar())

    def updateProgressBar(self, val):
        self.progressBar.setValue(val)


class ThreadClass(QtCore.QThread):
    def __init__(self, parent=None):
        super(ThreadClass, self).__init__(parent)

    def run(self):
        while True:
            val = test3_1.getCPU()
            self.emit(QtCore.SIGNAL('CPU_VALUE'), val)


if __name__ == '__main__':
    a = QApplication(sys.argv)
    app = MainUiClass()
    app.show()
    a.exec_()
