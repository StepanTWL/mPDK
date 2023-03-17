fix_error = []


def parse_answer(package: bytearray, rules: dict) -> list:
    global fix_error
    for i in rules.items():
        adr = i[0][:i[0].find('.')]
        bit = i[0][-1]
        val = i[1]
        if package[int()] & bit == val
    return frame

answer = bytearray(b'\x7c\xe6\x2e\x06')
rules = {
    '0.0': '0',
    '3.7': '1',
}

fix_error = parse_answer(answer, rules)