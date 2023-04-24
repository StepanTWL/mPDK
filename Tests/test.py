import serial.tools.list_ports
print([comport.device for comport in serial.tools.list_ports.comports()])


from serial.tools import list_ports
ports = list_ports.comports()

for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))