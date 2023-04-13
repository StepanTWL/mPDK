import sys
from time import time

import serial
from copy import copy
from PyQt5 import QtCore, uic, QtWidgets
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication
from errors import form_dict, errors

commands = []
rules_mask = dict()
frame = bytearray()
receive_size = 0
port = serial.Serial(port='COM6', baudrate=230400, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
delay = 0
cycle = 231  # 10ms


def read_code():
    str_commands = []
    text_commands = main.textEditCode.toPlainText()
    if text_commands[-1] != '\n':
        text_commands += '\n'
    while '\n' in text_commands:
        if text_commands.find('//') < text_commands.find('\n') and text_commands.find('//') != -1:
            str_commands.append(text_commands[:text_commands.index('//')])
        else:
            str_commands.append(text_commands[:text_commands.index('\n')])
        text_commands = text_commands[text_commands.index('\n') + 1:]
    for i in range(len(str_commands)):
        str_commands[i] = "".join(str_commands[i].split())
    return copy(str_commands)


def parse_function(s: str) -> bool:
    global frame, rules_mask, receive_size, delay
    command = s[:s.find('(')]
    match command:
        case 'transmit':
            if not delay:
                frame = function_transmit(s)
                return True
            # print(frame)
        case 'receive':
            if not delay:
                rules_mask, receive_size = function_receive(s)
                return True
            # print(rules_mask)
        case 'delay':
            delay = function_delay(s)
            return True
        case 'startEventHandling':
            pass


def parse_answer(package: bytearray, rules: dict) -> list:
    for i in rules.items():
        adr = int(i[0][:i[0].find('.')])
        bit = int(i[0][-1])
        val = int(i[1])
        if package[adr] & (1 << bit) == (val << bit):
            form_dict(f'Ошибка в байте {adr}, бит {bit}', val, True)
        else:
            form_dict(f'Ошибка в байте {adr}, бит {bit}', val, False)


def func(frame: bytearray, rules, rec_size: int = 16):  # period=0 - non cycle
    port.write(frame)
    answer = port.read(rec_size)
    parse_answer(answer, rules)


def parse_text_programm():
    global commands
    commands = read_code()
    for i in range(len(commands)):
        if parse_function(commands[i]):
            commands[i] = None
    func(frame, rules_mask, receive_size)


class ProgressbarWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi('window.ui', self)
        self.pushButtonStart.clicked.connect(self.start_worker)
        self.pushButtonStop.clicked.connect(self.stop_worker)

    def start_worker(self):
        self.thread = ThreadClass(parent=None, index=1)
        self.thread.start()
        self.thread.any_signal.connect(parse_text_programm)
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

    def my_delay(self, time_delay_start=[]):
        global delay
        if delay:
            if not time_delay_start:
                time_start = time()
                time_delay_start.append(time_start)
                return
            if (time() - time_delay_start[0]) * 1000 > delay:
                time_delay_start.pop()
                delay = 0
                if not None in commands:
                    return
                else:
                    self.stop_worker()


class ThreadClass(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(int)

    def __init__(self, parent=None, index=0):
        super(ThreadClass, self).__init__(parent)
        self.index = index
        self.is_running = True

    def run(self):
        global cycle
        cnt = 0
        while True:
            cnt += 1
            QThread.msleep(cycle)  # 2 and less begin bad
            self.any_signal.emit(cnt)

    def stop(self):
        self.is_running = False
        self.terminate()


app = QApplication(sys.argv)
main = ProgressbarWindow()
main.show()
sys.exit(app.exec_())
