import sqlite3
import uuid
import datetime

def Connect():
    conn = sqlite3.connect('siawiz.db')
    return conn

def CreateProject(name, description):
    conn = Connect()
    cur = con.cursor()
    id = uuid.uuid1()
    sql = "INSERT INTO projects(id,name,description,createddate) VALUES(?,?,?,?)"
    cur.execute(sql, id, name, description, datetime.datetime.utcnow())

def ListProjects():
    conn = Connect()
    cur = conn.cursor()
    cur.execute('SELECT * FROM projects')
    data = cur.fetchall()
    return data

def ListServices(id):
    conn = Connect()
    cur = conn.cursor()
    if id == "":
        cur.execute('SELECT s.*, p.name as [projectname] FROM services s LEFT OUTER JOIN projects p ON s.projectid = p.id')
    else:
        cur.execute('SELECT s.*, p.name as [projectname] FROM services s LEFT OUTER JOIN projects p ON s.projectid = p.id WHERE s.projectid=?', id)
    data = cur.fetchall()
    return data

def GetSetting():
    cur = conn.cursor()
    cur.execute('SELECT * FROM setting')
    data = cur.fetchone()
    setting = {"dd_folder": data[1], "dd_host": data[2], "dd_port": data[3]}
    return setting


