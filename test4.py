import datetime
from copy import copy

events = dict()


def form_dict(object, error_value, active):
    global events
    flag = False
    t = datetime.datetime.now()
    time = f'{str(t.hour).zfill(2)}:{str(t.minute).zfill(2)}:{str(t.second).zfill(2)}.{str(t.microsecond // 1000).zfill(3)}'
    if not hasattr(form_dict, '_count'):
        form_dict._count = 0
    arr = ['time_activ', 'time_deactiv', 'object', 'error_value', 'active']
    listt = [time, time, object, error_value, active]
    event_value = {i: listt[num] for num, i in enumerate(arr)}
    if not events:
        events[form_dict._count] = event_value
    else:
        for i in events.values():
            if i['object'] == object and i['error_value'] == error_value and i['active']:
                if not active:
                    i['time_deactiv'] = time
                    i['active'] = active
                if active:
                    i['time_deactiv'] = time
                flag = True
        if not flag:
            form_dict._count += 1
            events[form_dict._count] = event_value


def errors():
    global events
    return copy(events)


"""
form_dict('12:12:12.001', 'Ошибка! Байт 0, бит 0', 1, True)
form_dict('12:12:12.002', 'Ошибка! Байт 0, бит 1', 1, True)
form_dict('12:12:12.003', 'Ошибка! Байт 0, бит 1', 0, True)
form_dict('12:12:12.004', 'Ошибка! Байт 0, бит 0', 1, False)
form_dict('12:12:12.005', 'Ошибка! Байт 0, бит 1', 1, False)
form_dict('12:12:12.006', 'Ошибка! Байт 0, бит 1', 0, False)
form_dict('12:12:12.007', 'Ошибка! Байт 0, бит 0', 1, True)
form_dict('12:12:12.008', 'Ошибка! Байт 0, бит 1', 1, True)
form_dict('12:12:12.009', 'Ошибка! Байт 0, бит 1', 0, True)
form_dict('12:12:12.010', 'Ошибка! Байт 0, бит 0', 1, False)
form_dict('12:12:12.011', 'Ошибка! Байт 0, бит 1', 1, False)
form_dict('12:12:12.012', 'Ошибка! Байт 0, бит 1', 0, False)
print(events)
"""

"""
{
    0 : {
        'time_start'    : '12:12:12.001',
        'time_end'      : '12:12:11.001',
        'object'        : 'Ошибка! Байт 0, бит 0'
        'error_value'   : 1,
        'active'        : True,
        }
    1 : {
        'time_start'    : '12:12:12.002',
        'time_end'      : '12:12:11.002',
        'object'        : 'Ошибка! Байт 0, бит 1'
        'error_value'   : 1,
        'active'        : True,
        }
}
"""
