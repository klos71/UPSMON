from flask import Flask, request, redirect, url_for, render_template, g
from wtforms import Form, StringField, SubmitField
from wtforms.validators import DataRequired
import sqlite3
import temp as tp
#import snmp

app = Flask(__name__)

app.secret_key = 'super secret string'

DATABASE = "database.db"

class add_form(Form):
    name = StringField("name")
    ip = StringField("ip")
    submit = SubmitField('Add Ups')


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def error(errormsg):
    return render_template("error.html", error=errormsg)



def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def listBuilder():
    upses = []
    query = query_db("SELECT * FROM upses")
    for x in range(0, len(query),1):
        name = query[x][1]
        ip = query[x][6]
        serial = query[x][2]
        dc = query[x][3]
        batt = query[x][4]
        curr = query[x][5]
        battmfr = query[x][8]
        status = query[x][9]
        lastup= query[x][7]
        upsNumber = query[x][10]
        ups = dict(name=name, ip=ip, serial=serial, DC=dc,batt=batt,currpow=curr,battmfr=battmfr, lastup=lastup, status=status, nmr=upsNumber)
        upses.append(ups)
    return upses


@app.route('/')
def index():

    return render_template("index.html", amount=len(listBuilder()))

@app.route('/all')
def list_of_all():
    name = query_db("SELECT * FROM upses")
    return str(name)

@app.route('/upses')
def list():
    name = query_db("SELECT * FROM upses")
    return render_template("upses.html", upsList=listBuilder())


@app.route('/addups', methods=["GET", "POST"])
def add():
    form = add_form(request.form)
    if(request.method == "POST"):
        name = form.name.data
        ip = form.ip.data
        #snmp.createups()
        tp.updateUps(name,ip)
        return error("test")
    return render_template("addups.html", form=form)


@app.route('/removeups')
def remove():
    return render_template("removeups.html", upsList=listBuilder())


@app.context_processor
def utility_processor():
    def format_price(name,ip,number):
        #snmp.updateUps(name,ip,number)
        return 0
    return dict(format_price=format_price)

