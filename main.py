import datetime
import sys
import time
from copy import copy
from threading import Thread
from interface import port
from PyQt5 import QtWidgets
from window import Ui_MainWindow

commands = []
rules_mask = dict()
fix_error = []
frame = bytearray()
#port = serial.Serial(port='COM6', baudrate=230400, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)


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
    return copy(arr)


def formFrame(frame: str, size: int) -> bytearray:
    s = frame[1:-1].replace(' ', '').replace(',', ' ')
    while '(' in s:
        count = int(s[s.find('(') + 1:s.find(')')]) - 1
        number = s[s.find('(') - 2:s.find('(')]
        s = s[:s.find('(')] + (' ' + number) * count + s[s.find(')') + 1:]
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


def function_transmit(frame_str: str) -> bytearray:
    frame_bytes = bytearray()
    s = ''
    size = 0
    crc = ''

    s = frame_str[frame_str.find('['):frame_str.find(']') + 1]
    size = int(frame_str[frame_str.find('size=') + 5:frame_str.find(',', frame_str.find('size='), )])
    crc = frame_str[frame_str.find('crc32=') + 6:frame_str.rfind(',')]
    frame_bytes = formFrame(s, size)
    if crc == 'true':
        frame_bytes += crc32(frame_bytes)
    return copy(frame_bytes)


def function_receive(s: str) -> dict:
    string = ''.join(s.split())
    arr = list(map(str, string[string.find('[') + 1:string.rfind(']')].split(',')))
    for i in arr:
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
    return copy(rules_mask)


def parse_function(s: str):
    global frame, rules_mask
    command = s[:s.find('(')]
    match command:
        case 'transmit':
            frame = function_transmit(s)
            print(frame)
        case 'receive':
            rules_mask = function_receive(s)
            print(rules_mask)
        case 'delay':
            pass
        case 'startEventHandling':
            pass
    pass


def parse_text_programm():
    global commands;
    commands = read_code()
    for i in commands:
        parse_function(i)


def parse_answer(package: bytearray, rules: dict) -> list:
    frame = []
    for i in rules.items():
        adr = int(i[0][:i[0].find('.')])
        bit = int(i[0][-1])
        val = int(i[1])
        if package[adr] & (1 << bit) == val:
            t = datetime.datetime.now()
            frame.append(f'{t.hour}:{t.minute}:{t.second}:{t.microsecond // 1000} Байт {adr}, бит {bit} - {val}')
            pass
    return copy(frame)


def func(frame: bytearray, rules, error, receive_size: int = 16, period: int = 0):  # period=0 - non cycle
    while True:
        port.write(frame)
        answer = port.read(receive_size)
        error = parse_answer(answer, rules)
        print(error)
        if period:
            time.sleep(0.001 * period)
        else:
            break


th = Thread(target=func(frame, rules_mask, fix_error, 16, 1))
th.start()

app = QtWidgets.QApplication(sys.argv)
mPDK = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(mPDK)
mPDK.show()

ui.pushButtonStart.clicked.connect(parse_text_programm)
if (len(fix_error)):
    ui.textEditResult.setPlainText(fix_error)
    fix_error.clear()
sys.exit(app.exec_())
