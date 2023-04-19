class Command:
    instances_count = 0

    def __init__(self, transmit: str, receive: str, delay: str):
        Command.instances_count += 1
        self.queue = Command.instances_count
        self.transmit = transmit
        self.receive = receive
        self.delay = delay
        self.done = False

    @classmethod
    def form_table_crc32_jamcrc(cls) -> list[int]:
        table_crc32 = []
        for i in range(256):
            value = i
            for _ in range(8):
                value = (value >> 1) ^ 0xEDB88320 if value & 0x00000001 else value >> 1
            table_crc32.append(value)
        return table_crc32

    @classmethod
    def form_crc32(cls, frame_bytes: bytearray) -> bytearray:
        crc_table = cls.form_table_crc32_jamcrc()
        crc = 0xffffffff
        for byte in frame_bytes:
            crc = (crc >> 8) ^ crc_table[(crc ^ byte) & 0xFF]
        crc &= 0xFFFFFFFF
        return crc.to_bytes(4, byteorder='little')

    def form_transmit_frame(self) -> bytearray:
        tmp_str = self.transmit[9:-1]
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
        return int(self.receive[self.receive.find('size=') + 5:self.receive.find(')')])

    def form_rules(self) -> dict:  # receive([0:[1-4]=0], size=12)
        errors = dict()
        arr = list(map(str, self.receive[self.receive.find('[') + 1:self.receive.rfind(']')].split(',')))
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
        return int(self.delay[self.delay.find('(')+1:self.delay.find(')')])

    def set_done(self):
        self.done = True

    def get_done(self):
        return self.done


listt = ['transmit([0c, 00(7)], size=8, crc32=true)', 'receive([0:[1-4]=0, 1:[1-5]=1], size=12)', 'delay(1000)',
         'transmit([0c, 10(7)], size=8, crc32=true)', 'receive([2:[1-4]=0, 3:[1-5]=1], size=12)', 'delay(2000)']
current_deal = Command(listt[0], listt[1], listt[2])
if current_deal.done:
    print('Norm')


'''
if 'transmit' in listt[0] and 'receive' in listt[1] and 'delay' in listt[2]:
    current_deal = Command(listt[0], listt[1], listt[2])
    listt.pop(0)
    listt.pop(0)
    listt.pop(0)


print(current_deal.form_transmit_frame())
print(current_deal.get_receive_size())
print(current_deal.get_delay_ms())
print(current_deal.form_rules())
'''
