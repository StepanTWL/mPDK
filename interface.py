import time
import serial

#port = serial.Serial(port='COM6', baudrate=230400, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)

package = bytearray([0x0c, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7c, 0xe6, 0x2e, 0x06])
"""
def func(frame: bytearray, rules, error, receive_size: int = 16, period: int = 0):  # period=0 - non cycle
    while True:
        port.write(frame)
        #answer = port.read(receive_size)
        #error = parse_answer(answer, rules)
        print(error)
        if period:
            time.sleep(0.001 * period)
        else:
            break
    
th = Thread(target=func(frame, rules_mask, fix_error, 16, 1000))
th.start()
"""