from pysnmp.hlapi import *
import datetime, time, sqlite3
from flask import g

batteryTime = ""
batteryPrecent = ""
serial = ""
status = ""
batteryMfrDate = ""

DATABASE = "database.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def createUps(name,ip,upsnumber):
    conn = sqlite3.connect("database.db")
    conn.execute("INSERT INTO upses (upsname, ip, upsnumber) VALUES (?, ?, ?)", (name,ip,1))
    conn.commit()


def removeUps(name, ip, upsnumber):
    conn = sqlite3.connect("database.db")
    conn.execute("DELETE FROM upses WHERE upsname= ? ", name)
    conn.commit()

def updateUps(name, ip, upsnumber):

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    setVariables(upsnumber)
    print name
    print ip
    conn = sqlite3.connect("database.db")
    conn.execute("UPDATE upses SET Lastdc= ? WHERE upsname= ? ", (st,name))
    conn.commit()
    


def setVariables(upsNumber):
    global batteryTime
    global batteryPrecent
    global serial
    global status
    global batteryMfrDate
    if (upsNumber == 1):
        # OID for APC Pro 900, works with config in raspberry
        batteryTime = ".1.3.6.1.4.1.8072.1.3.2.3.1.1.12.117.112.115.46.114.117.110.116.105.109.101.49"
        batteryPrecent = ".1.3.6.1.4.1.8072.1.3.2.3.1.1.15.98.97.116.116.101.114.121.46.99.104.97.114.103.101.49"
        serial = ".1.3.6.1.4.1.8072.1.3.2.3.1.1.11.117.112.115.46.115.101.114.105.97.108.49"
        status = ".1.3.6.1.4.1.8072.1.3.2.3.1.1.11.117.112.115.46.115.116.97.116.117.115.49"
        batteryMfrDate = ".1.3.6.1.4.1.8072.1.3.2.3.1.1.15.98.97.116.116.101.114.121.46.109.102.114.100.97.116.101"
    elif (upsNumber == 2):
        # OID set 2
        batteryTime = ".1.3.6.1.4.1.8072.1.3.2.3.1.1.12.117.112.115.46.114.117.110.116.105.109.101.50"
        batteryPrecent = ".1.3.6.1.4.1.8072.1.3.2.3.1.1.15.98.97.116.116.101.114.121.46.99.104.97.114.103.101.50"
        serial = ".1.3.6.1.4.1.8072.1.3.2.3.1.1.11.117.112.115.46.115.101.114.105.97.108.50"
        status = ".1.3.6.1.4.1.8072.1.3.2.3.1.1.11.117.112.115.46.115.116.97.116.117.115.50"
        batteryMfrDate = ".1.3.6.1.4.1.8072.1.3.2.3.1.2.16.98.97.116.116.101.114.121.46.109.102.114.100.97.116.101.50"
    elif (upsNumber == 3):
        # OID set 3
        batteryTime = ".1.3.6.1.4.1.8072.1.3.2.3.1.1.12.117.112.115.46.114.117.110.116.105.109.101.51"
        batteryPrecent = ".1.3.6.1.4.1.8072.1.3.2.3.1.1.15.98.97.116.116.101.114.121.46.99.104.97.114.103.101.51"
        serial = ".1.3.6.1.4.1.8072.1.3.2.3.1.1.11.117.112.115.46.115.101.114.105.97.108.51"
        status = ".1.3.6.1.4.1.8072.1.3.2.3.1.1.11.117.112.115.46.115.116.97.116.117.115.51"
        batteryMfrDate = ".1.3.6.1.4.1.8072.1.3.2.3.1.2.16.98.97.116.116.101.114.121.46.109.102.114.100.97.116.101.51"


# gets batteryTime from given RaspberryPi ip TODO: get ip from database
def fetchBatteryTime(ip, upsnumber):
    # setVariables(int(upsnumber))
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('public', mpModel=0),
               UdpTransportTarget((ip, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(batteryTime)))
    )

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print(errorStatus.prettyPrint())
    else:
        for varBind in varBinds:
            temp = int(varBind[1])
            return temp / 60


# Same as abov but with precent
def fetchBatteryPrecent(ip, upsnumber):
    # setVariables(upsnumber)
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('public', mpModel=0),
               UdpTransportTarget((ip, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(batteryPrecent)))
    )

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print(errorStatus.prettyPrint())
    else:
        for varBind in varBinds:
            temp = int(varBind[1])
            return temp


def fetchDeviceSerial(ip, upsnumber):
    # setVariables(upsnumber)
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('public', mpModel=0),
               UdpTransportTarget((ip, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(serial)))
    )

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print(errorStatus.prettyPrint())
    else:
        for varBind in varBinds:
            temp = varBind[1]
            return temp


def fetchDeviceStatus(ip, upsnumber):
    # setVariables(upsnumber)
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('public', mpModel=0),
               UdpTransportTarget((ip, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(status)))
    )

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print(errorStatus.prettyPrint())
    else:
        for varBind in varBinds:
            temp = varBind[1]
            return temp


def fetchBatteryMfr(ip, upsnumber):
    # setVariables(upsnumber)
    print(ip)
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('public', mpModel=0),
               UdpTransportTarget((ip, 45161)),
               ContextData(),
               ObjectType(ObjectIdentity(batteryMfrDate)))
    )

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print(errorStatus.prettyPrint())
    else:
        for varBind in varBinds:
            temp = varBind[1]
            return temp

setVariables(1)
fetchBatteryMfr("85.134.54.92", 1)