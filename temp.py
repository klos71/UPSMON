import sqlite3, time, datetime
from flask import g


def updateUps(name, ip):
    #print str(name)
    #print str(ip)
    conn = sqlite3.connect("database.db")
    conn.execute("INSERT INTO upses (upsname, ip, upsnumber) VALUES (?, ?, ?)", (name, ip, 1))
    conn.commit()

def updateall(name,ip):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    #setVariables(upsnumber)
    #print name
    #print ip
    conn = sqlite3.connect("database.db")
    conn.execute("UPDATE upses SET Lastdc= ? WHERE upsname= ? ", (st, name))
    conn.commit()

