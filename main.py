import sys
from time import time
import serial
from PyQt5 import QtCore, uic, QtWidgets
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QMenu
from Tests.test5 import Command
from errors import form_dict, errors

port = serial.Serial(port='COM6', baudrate=230400, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
commands = []
current_deal = None
cycle = 321


def read_code():
    array_commands = []
    text_commands = main.textEditCode.toPlainText()
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


def check_answer(package: bytearray, rules: dict):
    for i in rules.items():
        adr = int(i[0][:i[0].find('.')])
        bit = int(i[0][-1])
        val = int(i[1])
        if package[adr] & (1 << bit) == (val << bit):
            form_dict(f'Ошибка в байте {adr}, бит {bit}', val, True)
        else:
            form_dict(f'Ошибка в байте {adr}, бит {bit}', val, False)


def interface(transmit_frame: bytearray, rules: dict, receive_size: int):
    port.write(transmit_frame)
    answer = port.read(receive_size)
    check_answer(answer, rules)


def work_programm():
    global commands, current_deal
    if len(commands) == 0 and not current_deal:
        commands = read_code()
    elif len(commands) == 0 and current_deal.get_done():
        main.stop_worker()
        current_deal = None
        return
    if len(commands) > 1 and (not current_deal or not current_deal.done):
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
        self.ui = uic.loadUi('window.ui', self)
        self.pushButtonStart.clicked.connect(self.start_worker)
        self.pushButtonStop.clicked.connect(self.stop_worker)

    def start_worker(self):
        self.thread = ThreadClass(parent=None, index=1)
        self.thread.start()
        self.thread.any_signal.connect(work_programm)
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
        global current_deal
        if current_deal and current_deal.get_delay_ms():
            if not len(time_delay_start):
                time_delay_start.append(time())
                return
            if (time() - time_delay_start[0]) * 1000 > current_deal.get_delay_ms():
                time_delay_start.pop()
                current_deal.delay = 0
                current_deal.set_done()


    def contextMenuEvent(self, event) -> None:
        contextMenu = QMenu(self)

        clearAction = contextMenu.addAction('Clear all')
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))

        if action == clearAction:
            self.close()


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
