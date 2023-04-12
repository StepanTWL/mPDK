class Command:
    instances_count = 0

    def __init__(self, transmit: str, receive_size: int, errors: dict, delay: int = 0):
        Command.instances_count += 1
        self.queue = Command.instances_count
        self.transmit = transmit
        self.transmit_size = 0
        self.receive_frame = bytearray()
        self.receive_size = receive_size
        self.errors = errors
        self.delay = delay

    def form_transmit_frame(self):  # transmit([0c, 10(7)], size=8, crc32=true, cycle=true)
        tmp_str = self.transmit.replace(' ', '')
        tmp_str = tmp_str[9:-1]
        while '(' in tmp_str:  # [0c,10(7)],size=8,crc32=true,cycle=true
            count_byte = int(tmp_str[tmp_str.find('(') + 1:tmp_str.find(')')])-1
            number = tmp_str[tmp_str.find('(') - 2:tmp_str.find('(')]
            tmp_str = tmp_str[:tmp_str.find('(')] + (',' + number) * count_byte + tmp_str[tmp_str.find(')') + 1:]
        size = int(tmp_str[tmp_str.find('size=') + 5:tmp_str.find(',', tmp_str.find('size='))])
        if size > tmp_str.count(',', tmp_str.find('['), tmp_str.find(']')) + 1:  # [0c,10,10,10,10,10,10,10],size=8,crc32=true,cycle=true
            count_byte = size - tmp_str.count(',', tmp_str.find('['), tmp_str.find(']')) - 1
            tmp_str = tmp_str[tmp_str.find('[')+1:tmp_str.find(']')] + ',00' * count_byte
        else:
            tmp_str = tmp_str[tmp_str.find('[') + 1:tmp_str.find(']')]
        tmp_str = tmp_str.replace(',', ' ')
        return bytearray.fromhex(tmp_str)

a = Command('transmit([0c, 10(7)], size=8, crc32=true, cycle=true)', 1, {'1':'1'})
print(a.form_transmit_frame())