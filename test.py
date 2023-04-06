import datetime

fix_error = []


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
    return frame


answer = bytearray(b'\x7c\xe6\x2e\x06')
rules = {
    '0.0': '0',
    '0.1': '0',
    '0.2': '0',
    '0.3': '0',
    '3.7': '1',
}

fix_error = parse_answer(answer, rules)
for _ in fix_error:
    print(_)

def ascii_to_hex(s: str):
    s1 = bytes.fromhex(s).decode()
    return str.encode(s1)