from datetime import time
from threading import Thread

from interface import port
from main import parse_answer


def func(frame: bytearray, rules, period: int = 0):  # period=0 - non cycle
    package = bytearray([0x0c, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7c, 0xe6, 0x2e, 0x06])

    while True:
        port.write(frame)
        answer = port.read(size=16)
        # result = parse_answer(answer, rules)
        result = parse_answer(package, rules)
        if period:
            time.sleep(0.001 * period)
        else:
            break

th = Thread(target=func())
th.start()