import sys
from copy import copy

from PyQt5 import QtWidgets
from window import Ui_MainWindow

arr_commands = []
def on_click_start():
    global arr_commands
    arr = []
    s = ui.textEditCode.toPlainText()
    if s[-1] != '\n':
        s = s+'\n'
    while '\n' in s:
        if s.find('//') < s.find('\n') and s.find('//') != -1:
            arr.append(s[:s.index('//')])
        else:
            arr.append(s[:s.index('\n')])
        s = s[s.index('\n')+1:]
    for i in range(len(arr)):
        arr[i] = "".join(arr[i].split())
    arr_commands = copy(arr)
    pass

def function_transmit(size:int, crc32:str, cycle:str):
    pass


app = QtWidgets.QApplication(sys.argv)
mPDK = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(mPDK)
mPDK.show()

ui.pushButtonStart.clicked.connect(on_click_start)
sys.exit(app.exec_())
