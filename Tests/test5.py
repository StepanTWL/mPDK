from time import time


def my_delay(delay, time_delay_start=[]):
    while True:
        if not time_delay_start:
            time_start = time()
            time_delay_start.append(time_start)
            continue
        if (time() - time_delay_start[0]) * 1000 > delay:
            return

print(time())
my_delay(1000)
print(time())