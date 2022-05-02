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

#Show all prereq of electives and required classes for this degree
def majorPrereq(degree):
    cur = connectToDB()
    query = "SELECT classID, preReq FROM Requirements WHERE gradReq LIKE '%%' || %s || '%%'"
    cur.execute(query, (degree,))
    return cur.fetchall()

#Subject Example: CSE, MATH
def allClassesInMajor(major):
    cur = connectToDB()
    query = "SELECT * FROM Classes WHERE classID LIKE '%%' || %s || '%%'"
    cur.execute(query, (major,))
    return cur.fetchall()

# all attributes for single class
def singleClass(className):
    cur = connectToDB()
    query = "SELECT * FROM Requirements WHERE classID = %s"
    cur.execute(query, (className,))
    return cur.fetchall()
# credit
def singleClassCredit(classID):
    cur = connectToDB()
    query = "SELECT credit FROM Classes WHERE classID = %s"
    cur.execute(query, (classID,))
    return cur.fetchall()

# quarters
def singleClassQuarters(classID):
    cur = connectToDB()
    query = "SELECT quarters FROM Classes WHERE classID = %s"
    cur.execute(query, (classID,))
    return cur.fetchall()

# for frontend search bar
# all classes with attribute classname, subject, credit, quarter
def allClassesByClassName(className, degree):
    cur = connectToDB()
    query = "SELECT DISTINCT className, subject, credit, quarters FROM Classes, Requirements WHERE className LIKE '%%' || %s || '%%' AND Classes.classID = Requirements.classID AND gradReq LIKE '%%' || %s || '%%'"
    cur.execute(query, (className, degree,))
    return cur.fetchall()

print(allClassesByClassName('MATH', 'Computer Science B.S'))