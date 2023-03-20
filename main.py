import sys
import time
from copy import copy
from threading import Thread
from typing import List, Dict

from PyQt5 import QtWidgets

from interface import port
from window import Ui_MainWindow

arr_commands = []
rules_mask = dict()
fix_error = []

def create_table_crc32_jamcrc():
    a = []
    for i in range(256):
        k = i
        for _ in range(8):
            k = (k >> 1) ^ 0xEDB88320 if k & 0x00000001 else k >> 1
        a.append(k)
    return a


def crc32_jamcrc(frame):
    crc_table = create_table_crc32_jamcrc()
    crc = 0xffffffff
    for byte in frame:
        crc = (crc >> 8) ^ crc_table[(crc ^ byte) & 0xFF]
    return crc & 0xFFFFFFFF


def ascii_to_hex(s: str):
    s1 = bytes.fromhex(s).decode()
    return str.encode(s1)


def read_code():
    global arr_commands
    arr = []
    s = ui.textEditCode.toPlainText()
    if s[-1] != '\n':
        s = s + '\n'
    while '\n' in s:
        if s.find('//') < s.find('\n') and s.find('//') != -1:
            arr.append(s[:s.index('//')])
        else:
            arr.append(s[:s.index('\n')])
        s = s[s.index('\n') + 1:]
    for i in range(len(arr)):
        arr[i] = "".join(arr[i].split())
    arr_commands = copy(arr)
    pass


def formFrame(frame: str, size: int) -> bytearray:
    s = frame[1:-1].replace(' ', '').replace(',', ' ')
    while '(' in s:
        count = int(s[s.find('(') + 1:s.find(')')]) - 1
        number = s[s.rfind(' ', 0, s.find('(')):s.find('(')]
        s = s[:s.find('(')] + (' ' + number) * count + s[s.find(')'):]
    if size > s.count(' ') + 1:
        count = size - s.count(' ') - 1
        s += ' 00' * count
    package = bytearray.fromhex(s)
    return package


def crc32(frame: bytearray):
    tmp = bytearray()
    crc_table = create_table_crc32_jamcrc()
    crc = 0xffffffff
    for byte in frame:
        crc = (crc >> 8) ^ crc_table[(crc ^ byte) & 0xFF]
    crc &= 0xFFFFFFFF
    tmp = crc.to_bytes(4, byteorder='little')
    if tmp == bytearray(b'\x7c\xe6\x2e\x06'):
        pass
    return tmp


def function_transmit(s: str):
    frame_ = bytearray()
    frame = ''
    size = 0
    crc = ''

    frame = s[s.find('['):s.find(']') + 1]
    size = int(s[s.find('size=') + 5:s.find(',', s.find('size='), )])
    crc = s[s.find('crc32=') + 6:s.rfind(',')]
    frame_ = formFrame(frame, size)
    if crc == 'true':
        frame_ += crc32(frame_)
    transfer_data(frame_, 500)


# receive([10:[1]=0, 12:[1-8]=1, 14:[1]=0])
def function_receive(s: str):
    global rules_mask
    rulse = ''.join(s.split())
    rulse = list(map(str, rulse[rulse.find('[') + 1:rulse.rfind(']')].split(',')))
    for i in rulse:
        bits = i[i.find('[') + 1:i.find(']')]
        byte = i[:i.find(':')]
        value = i[-1]
        if '-' in bits:
            start = bits[0]
            stop = bits[-1]
            for j in range(int(start), int(stop) + 1):
                rules_mask[byte + '.' + str(j)] = value
        else:
            rules_mask[byte + '.' + bits] = value


def parse_function(s: str):
    command = s[:s.find('(')]
    match command:
        case 'transmit':
            function_transmit(s)
        case 'receive':
            function_receive(s)
        case 'delay':
            pass
        case 'startEventHandling':
            pass
    pass


def parse_programm():
    read_code()
    for i in arr_commands:
        parse_function(i)
    pass


def transfer_data(package: bytearray, delay_ms: int):
    global fix_error, rules_mask
    port.write(package)
    answer = port.read(size=16)
    #fix_error = parse_answer(answer, rules_mask)
    time.sleep(delay_ms * 0.001)


def func(frame: bytearray, rules, period: int = 0):  # period=0 - non cycle
    # package = bytearray([0x0c, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7c, 0xe6, 0x2e, 0x06])
    while True:
        port.write(frame)
        answer = port.read(size=16)
        #result = parse(answer, rules)
        if period:
            time.sleep(0.001 * period)
        else:
            break


#th = Thread(target=func(1))
#th.start()

app = QtWidgets.QApplication(sys.argv)
mPDK = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(mPDK)
mPDK.show()

ui.pushButtonStart.clicked.connect(parse_programm)
sys.exit(app.exec_())

# 0c 00 01 00 e8 03 00 00 f2 31 a3 17
