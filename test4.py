import sys
import time
from PyQt5 import QtCore, uic, QtWidgets
from PyQt5.QtWidgets import QApplication
import psutil


def getCPU():
    return  psutil.cpu_percent(interval=1)


class ProgressbarWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi('test4.ui', self)
        self.resize(888, 200)

        self.pushButton_start.clicked.connect(self.start_worker)
        self.pushButton_stop.clicked.connect(self.stop_worker)

    def start_worker(self):
        self.thread = ThreadClass(parent=None, index=1)
        self.thread.start()
        self.thread.any_signal.connect(self.my_function)
        self.pushButton_start.setEnabled(False)

    def stop_worker(self):
        if not self.pushButton_start.isEnabled():
            self.thread.stop()
        self.pushButton_start.setEnabled(True)

    def my_function(self, counter):
        cnt = counter
        index = self.sender().index
        if index == 1:
            self.progressBar.setValue(cnt)


class ThreadClass(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(int)

    def __init__(self, parent=None, index=0):
        super(ThreadClass, self).__init__(parent)
        self.index = index
        self.is_running = True

    def run(self):
        while True:
            time.sleep(0.02)
            self.any_signal.emit(int(getCPU()))

    def stop(self):
        self.is_running = False
        self.terminate()


app = QApplication(sys.argv)
main = ProgressbarWindow()
main.show()
sys.exit(app.exec_())
