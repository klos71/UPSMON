import sqlite3

DATABASE = "database.db"

def database():
    global conn, cursor
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `upses` (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, upsname TEXT, serial TEXT, Lastdc TIMESTAMP, battime INT, currpower INT, ip TEXT, lastupdate TIMESTAMP, battmfr DATE, status TEXT, upsnumber INT, mailflag INT)")
    conn.commit()
    print("Do you want to insert dummy data?? \n [1] Yes\n [2]No")
    choice = input()
    print(type(choice))
    if(choice == "1"):
        cursor.execute("INSERT INTO upses (upsname, serial, currpower, ip, status, upsnumber) VALUES ('Hylla1', '4B1805P27725','100', '192.168.1.1','OL','1')")
        cursor.execute("INSERT INTO upses (upsname, serial, currpower, ip, status, upsnumber) VALUES ('Hylla1-1', '4B1805P27726','100', '192.168.1.1','OB','2')")
        cursor.execute("INSERT INTO upses (upsname, serial, currpower, ip, status, upsnumber) VALUES ('Hylla2', '4B1805P27727','100', '192.168.1.2','ALARM','1')")
        conn.commit()
    else:
        print("Installation complete")

database()