import datetime
import sqlite3
from copy import copy
import datetime

bd = sqlite3.connect("base.sqlite")
cur = bd.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS errors(time_end TEXT, time_start TEXT, event TEXT, status INTEGER, active INTEGER)")
cur.execute("DELETE FROM errors")


def insert_event(event: str, status: int, active: int):
    isActive = False
    result = get_all_events()
    t = datetime.datetime.now()
    time_end = f'{str(t.hour).zfill(2)}:{str(t.minute).zfill(2)}:{str(t.second).zfill(2)}.{str(t.microsecond // 1000).zfill(3)}'
    if not len(result) and active:
        cur.execute("INSERT INTO errors VALUES (?, ?, ?, ?, ?)", (time_end, None, event, status, active))
    elif len(result) and active:
        for i in result:
            if i[2] == event and i[3] == status:
                if not i[1]:
                    cur.execute(f"UPDATE errors SET time_start = '{i[0]}' WHERE event = '{event}'")
                cur.execute(f"UPDATE errors SET time_end = '{time_end}' WHERE event = '{event}'")
                isActive = True
                break
        if not isActive:
            cur.execute("INSERT INTO errors VALUES (?, ?, ?, ?, ?)", (time_end, None, event, status, active))
    elif len(result) and not active:
        for i in result:
            if i[2] == event and i[3] == status:
                if not i[1]:
                    cur.execute(f"UPDATE errors SET time_start = '{i[0]}' WHERE event = '{event}'")
                cur.execute(f"UPDATE errors SET time_end = '{time_end}' WHERE event = '{event}'")
                cur.execute(f"UPDATE errors SET active = {active} WHERE event = '{event}'")
                break
    bd.commit()


def get_all_events():
    cur.execute("SELECT * FROM errors")
    result = cur.fetchall()
    return copy(result)

"""
arr = ['time_start', 'time_end', 'event', 'error_value', 'active']

def form_dict(time, event, error_value, active):
    

{
    0 : {
        'time_start'    : '12:12:12.001',
        'time_end'      : '12:12:11.001',
        'event'         : 'Ошибка! Байт 0, бит 0'
        'error_value'   : 1,
        'active'        : True,
        }
    1 : {
        }
}
"""