import psycopg2
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#psql postgres
#\c to check `CURRENT_USER`
#Create username with: CREATE USER postgres;
#grant `CURRENT_USER` to postgres;
#Postgres login: psql -d postgres -U postgres

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost/5432'

# db = SQLAlchemy(app)

# major = Majors.query.all()
def connectToDB():
    conn = psycopg2.connect('dbname=postgres user=postgres host=localhost', options='-c search_path=Majors')
    return conn.cursor()

def majorPrereq(degree):
    cur = connectToDB()
    value = degree
    query = "SELECT classID, preReq FROM Requirements WHERE gradReq LIKE '%%' || %s || '%%'"
    cur.execute(query, (value,))

    return cur.fetchall()

def singleClass(className):
    cur = connectToDB()
    value = className
    query = "SELECT * FROM Classes WHERE classID = %s"
    cur.execute(query, (value,))

    return cur.fetchall()

def allClassesInSubject(subject):
    cur = connectToDB()
    value = subject
    query = "SELECT * FROM Classes WHERE subject LIKE '%%' || %s || '%%'"
    cur.execute(query, (value,))

    return cur.fetchall()
print(majorPrereq('Computer Science B.S'))