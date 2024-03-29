import sys
import serial
import pydantic
from time import time
from PyQt5 import QtCore, uic, QtWidgets, QtGui
from serial.tools import list_ports
from command import Command
from errors import form_dict, errors, clear_errors

commands = []
current_deal = None


def search_port_upm():
    ports = list_ports.comports()
    arr_ports = []
    for portN, desc, _ in sorted(ports):
        if 'Virtual' in desc:
            arr_ports.append(portN)
    return arr_ports


arr_ports = search_port_upm()
if arr_ports:
    try:
        port = serial.Serial(port=arr_ports[0], baudrate=230400, timeout=0.002)
    except serial.SerialException:
        arr_ports.clear()


def read_code():
    array_commands = []
    text_commands = main.textEditCode.toPlainText()
    if not text_commands:
        return
    if text_commands[-1] != '\n':
        text_commands += '\n'
    while '\n' in text_commands:
        if text_commands.find('//') < text_commands.find('\n') and text_commands.find('//') != -1:
            array_commands.append(text_commands[:text_commands.index('//')])
        else:
            array_commands.append(text_commands[:text_commands.index('\n')])
        text_commands = text_commands[text_commands.index('\n') + 1:]
    for i in range(len(array_commands)):
        array_commands[i] = "".join(array_commands[i].split())
    return array_commands


def check_answer(package: bytes, rules: dict):
    for i in rules.items():
        adr = int(i[0][:i[0].find('.')])
        bit = int(i[0][-1])
        val = int(i[1])
        if package[adr] & (1 << bit) == (val << bit):
            form_dict(f'Ошибка в байте {adr}, бит {bit}', val, True)
        else:
            form_dict(f'Ошибка в байте {adr}, бит {bit}', val, False)


def interface(transmit_frame: bytearray, rules: dict, receive_size: int = 400):
    port.write(transmit_frame)
    if not receive_size:
        receive_size = 400
    answer = port.read(receive_size)
    check_answer(answer, rules)


def work_code():
    global commands, current_deal
    if (not commands or len(commands) == 0) and not current_deal:
        commands = read_code()
        if not commands:
            return
    elif len(commands) == 0 and current_deal.get_done():
        main.stop_worker()
        current_deal = None
        return
    if len(commands) > 1 and (not current_deal or current_deal.done):
        if 'transmit' in commands[0] and 'receive' in commands[1]:
            if len(commands) == 2:
                current_deal = Command(commands[0], commands[1], 'delay(0)')
                commands.pop(0)
                commands.pop(0)
            elif len(commands) > 2 and 'delay' in commands[2]:
                current_deal = Command(commands[0], commands[1], commands[2])
                commands.pop(0)
                commands.pop(0)
                commands.pop(0)
            elif len(commands) > 2 and not 'delay' in commands[2]:
                current_deal = Command(commands[0], commands[1], 'dela(0)')
                commands.pop(0)
                commands.pop(0)
    interface(current_deal.form_transmit_frame(), current_deal.form_rules(), current_deal.get_receive_size())


class ProgressbarWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.thread = None
        self.thread1 = None
        self.thread2 = None
        self.ui = uic.loadUi('window.ui', self)
        self.pushButtonStart.clicked.connect(self.start_worker)
        self.pushButtonStop.clicked.connect(self.stop_worker)
        self.textEditCode.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.textEditResult.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.textEditCode.customContextMenuRequested.connect(lambda: self.__contextMenu(self.textEditCode, None))
        self.textEditResult.customContextMenuRequested.connect(lambda: self.__contextMenu(self.textEditResult, clear_errors))
        if arr_ports:
            self.comboBox.addItems(arr_ports)
            self.comboBox.setCurrentIndex(0)

    def start_worker(self):
        self.thread = ThreadClass(parent=None, index=1)
        self.thread.start()
        self.thread.any_signal.connect(work_code)
        self.thread1 = ThreadClass(parent=None, index=2)
        self.thread1.start()
        self.thread1.any_signal.connect(self.my_function)
        self.thread2 = ThreadClass(parent=None, index=3)
        self.thread2.start()
        self.thread2.any_signal.connect(lambda _: self.my_delay())
        self.pushButtonStart.setEnabled(False)

    def stop_worker(self):
        if not self.pushButtonStart.isEnabled():
            self.thread.stop()
            self.thread1.stop()
            self.thread2.stop()
        self.pushButtonStart.setEnabled(True)

    def my_function(self, counter):
        index = self.sender().index
        result = errors()
        if index == 2:
            self.textEditResult.clear()
            for i in result.values():
                self.textEditResult.appendPlainText(
                    f"{i['time_activ']} {i['time_deactiv'].rjust(15)} {(i['object']).rjust(30)} - {str(i['error_value'])}")

    @classmethod
    def my_delay(cls, time_delay_start=[]):
        global current_deal
        if current_deal and current_deal.get_delay_ms():
            if not len(time_delay_start):
                time_delay_start.append(time())
                return
            if (time() - time_delay_start[0]) * 1000 > current_deal.get_delay_ms():
                time_delay_start.pop()
                current_deal.delay = 0
                current_deal.set_done()

    def __contextMenu(self, QPlainTextEdit, FunctionClear):
        QPlainTextEdit._normalMenu = QPlainTextEdit.createStandardContextMenu()
        self._addCustomMenuItems(QPlainTextEdit._normalMenu, QPlainTextEdit, FunctionClear)
        QPlainTextEdit._normalMenu.exec_(QtGui.QCursor.pos())

    def _addCustomMenuItems(self, menu, QPlainTextEdit, FunctionClear):
        menu.addSeparator()
        menu.addAction(u'Clear all', lambda: self.testFunc(QPlainTextEdit, FunctionClear))

    @classmethod
    def testFunc(cls, QPlainTextEdit, FunctionClear):
        QPlainTextEdit.clear()
        if FunctionClear:
            FunctionClear()


class ThreadClass(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(int)

    def __init__(self, parent=None, index=0):
        super(ThreadClass, self).__init__(parent)
        self.index = index
        self.is_running = True

    def run(self):
        cnt = 0
        while True:
            cnt += 1
            QtCore.QThread.msleep(2)
            self.any_signal.emit(cnt)

    def stop(self):
        self.is_running = False
        self.terminate()


app = QtWidgets.QApplication(sys.argv)
main = ProgressbarWindow()
main.show()
sys.exit(app.exec_())
