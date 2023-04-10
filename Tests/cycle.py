"""
from datetime import time
from threading import Thread
import serial
from main import parse_answer

port = serial.Serial(port='COM6', baudrate=230400, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)


#frame: bytearray, rules, period: int = 0
def func():  # period=0 - non cycle
    package = bytearray([0x0c, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7c, 0xe6, 0x2e, 0x06])
    rules = {
        '0.0': '0',
        '0.1': '0',
        '0.2': '0',
        '0.3': '0',
        '3.7': '1',
    }
    period = 1 #ms

    while True:
        port.write(package)
        answer = port.read(size=16)
        result = parse_answer(package, rules)
        if package:
            time.sleep(0.001 * period)
        else:
            break


th = Thread(target=func())
th.start()
"""