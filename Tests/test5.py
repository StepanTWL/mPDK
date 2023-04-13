class Command:
    instances_count = 0

    def __init__(self, transmit: str, receive: str, delay: str):
        Command.instances_count += 1
        self.queue = Command.instances_count
        self.transmit = transmit
        self.receive = receive
        self.delay = delay
        self.done = False

    def form_transmit_frame(self) -> bytearray:
        tmp_str = self.transmit.replace(' ', '')
        tmp_str = tmp_str[9:-1]
        while '(' in tmp_str:
            count_byte = int(tmp_str[tmp_str.find('(') + 1:tmp_str.find(')')]) - 1
            number = tmp_str[tmp_str.find('(') - 2:tmp_str.find('(')]
            tmp_str = tmp_str[:tmp_str.find('(')] + (',' + number) * count_byte + tmp_str[tmp_str.find(')') + 1:]
        size = int(tmp_str[tmp_str.find('size=') + 5:tmp_str.rfind(',')])
        if size > tmp_str.count(',', tmp_str.find('['), tmp_str.find(']')) + 1:
            count_byte = size - tmp_str.count(',', tmp_str.find('['), tmp_str.find(']')) - 1
            tmp_str = tmp_str[tmp_str.find('[') + 1:tmp_str.find(']')] + ',00' * count_byte
        else:
            tmp_str = tmp_str[tmp_str.find('[') + 1:tmp_str.find(']')]
        tmp_str = tmp_str.replace(',', ' ')
        if 'true' in self.transmit:
            return bytearray.fromhex(tmp_str) + self.form_crc32(bytearray.fromhex(tmp_str))
        else:
            return bytearray.fromhex(tmp_str)

    def get_receive_size(self) -> int:
        tmp_str = self.receive.replace(' ', '')
        return int(tmp_str[tmp_str.find('size=') + 5:tmp_str.find(')')])

    def form_errors(self) -> dict:  # receive([0:[1-4]=0], size=12)
        errors = dict()
        tmp_str = self.receive.replace(' ', '')
        arr = list(map(str, tmp_str[tmp_str.find('[') + 1:tmp_str.rfind(']')].split(',')))
        for i in arr:
            bits = i[i.find('[') + 1:i.find(']')]
            byte = i[:i.find(':')]
            value = i[-1]
            if '-' in bits:
                start = bits[0]
                stop = bits[-1]
                for j in range(int(start), int(stop) + 1):
                    errors[byte + '.' + str(j)] = value
            else:
                errors[byte + '.' + bits] = value
        return errors

    def get_delay_ms(self):
        tmp_str = self.delay.replace(' ', '')
        return int(tmp_str[tmp_str.find('(')+1:tmp_str.find(')')])

    def form_table_crc32_jamcrc(self) -> list[int]:
        table_crc32 = []
        for i in range(256):
            value = i
            for _ in range(8):
                value = (value >> 1) ^ 0xEDB88320 if value & 0x00000001 else value >> 1
            table_crc32.append(value)
        return table_crc32

    def form_crc32(self, frame_bytes: bytearray) -> bytearray:
        crc_table = self.form_table_crc32_jamcrc()
        crc = 0xffffffff
        for byte in frame_bytes:
            crc = (crc >> 8) ^ crc_table[(crc ^ byte) & 0xFF]
        crc &= 0xFFFFFFFF
        return crc.to_bytes(4, byteorder='little')


a = Command('transmit([0c, 10(7)], size=8, crc32=true)', 'receive([0:[1-4]=0, 1:[1-5]=1], size=12)', 'delay(1000)')
print(a.form_transmit_frame())
print(a.get_receive_size())
print(a.get_delay_ms())
print(a.form_errors())

