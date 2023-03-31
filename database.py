import sqlite3
bd = sqlite3.connect("base.sqlite")
cur = bd.cursor()
cur.execute("CREATE TABLE if NOT EXISTS errors(time TEXT, event TEXT, active INTEGER)")
cur.execute("DELETE FROM errors")

def insert_event(time: str, event: str):
    result = get_all_events()
    print(type(result[0]))
    cur.execute("INSERT INTO errors VALUES (?, ?)", (time, event))
    bd.commit()

def get_all_events():
    cur.execute("SELECT time, event FROM errors")
    result = cur.fetchall()
    return result

#print(result)
#cur.close()