import sys
from copy import copy
from typing import List

from PyQt5 import QtWidgets
from window import Ui_MainWindow

arr_commands = []


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

#s = str(hex(crc32_jamcrc(ascii_to_hex('0c 00 00 00 00 00 00 00'))))[2:].zfill(8)
#chunks = [s[i - 1:i + 1] for i in range(7, 0, -2)]
#print(chunks)

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


# 0c 10(7) size=10 -> 0c 10 10 10 10 10 10 10 00 00
# 0c size=8 -> 0c 00 00 00 00 00 00 00
def formFrame(frame: str, size: int) -> bytearray:
    s = frame[1:-1].replace(' ', '').replace(',', ' ')
    while '(' in s:
        count = int(s[s.find('(') + 1:s.find(')')]) - 1
        number = s[s.rfind(' ', 0, s.find('(')):s.find('(')]
        s = s[:s.find('(')] + (' ' + number) * count + s[s.find(')'):]
    if size > s.count(' ') + 1:
        count = size - s.count(' ') - 1
        s += ' 00' * count
    # 0c 10 10 10 10 10 10 10 00 00
    package = bytearray.fromhex(s)
    return package


def crc32(frame):
    tmp = bytearray()
    crc_table = create_table_crc32_jamcrc()
    crc = 0xffffffff
    for byte in frame:
        crc = (crc >> 8) ^ crc_table[(crc ^ byte) & 0xFF]
    crc &= 0xFFFFFFFF
    tmp = crc.to_bytes(length=4, byteorder='little')
    frame += tmp
    pass



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

#receive(size=56, [10[1]=0, 12[1-8]=0/1, 14[1,5]=1/0]) fiksiruet izmenenie bita nachinaet s 0 (u 3 s 1)
#receive(size=8, [0[0]=0])
def function_receive(s: str):
    size = 0
    follow = ''

    size = int(s[s.find('size=')+5:s.find(',')])
    follow = s[s.find('['):s.rfind(']')-1]


    pass


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


app = QtWidgets.QApplication(sys.argv)
mPDK = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(mPDK)
mPDK.show()

ui.pushButtonStart.clicked.connect(parse_programm)
sys.exit(app.exec_())
