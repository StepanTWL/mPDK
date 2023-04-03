import datetime
import sqlite3
from copy import copy
import datetime

bd = sqlite3.connect("base.sqlite")
cur = bd.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS errors(time_end TEXT, time_start TEXT, event TEXT, status INTEGER, active INTEGER)")
cur.execute("DELETE FROM errors")


def insert_event(event: str, status: int, active: int):
    result = get_all_events()
    t = datetime.datetime.now()
    time_end = f'{str(t.hour).zfill(2)}:{str(t.minute).zfill(2)}:{str(t.second).zfill(2)}.{str(t.microsecond // 1000).zfill(3)}'
    if result is None and active:
        cur.execute("INSERT INTO errors VALUES (?, ?, ?, ?, ?)", (time_end, 0, event, status, active))
    elif result is not None and active:
        for i in result:
            if i[2] == event and i[3] == status and active:
                cur.execute(f"UPDATE errors SET time_start = '{i[0]}' WHERE event = '{event}'")
                cur.execute(f"UPDATE errors SET time_end = '{time_end}' WHERE event = '{event}'")
            elif i[2] == event and i[3] == status and not active:
                pass
    cur.execute("INSERT INTO errors VALUES (?, ?, ?, ?, ?)", (time, 0, event, status, 1))
    bd.commit()


def get_all_events():
    cur.execute("SELECT * FROM errors")
    result = cur.fetchall()
    return copy(result)
