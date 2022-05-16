import psycopg2
#psql postgres
#\c to check `CURRENT_USER`
#Create username with: CREATE USER postgres;
#grant `CURRENT_USER` to postgres;
#Postgres local login: psql -d postgres -U postgres
#Heroku remote login: psql --dbname=dckbguanuf8a45 port=5432 --user=uxoitcpyfpqfvq --host=ec2-44-196-223-128.compute-1.amazonaws.com
#Heroku password: f646a5b031a7b5f570ef097d77f987809613ca53ee77167d1430d246105a0a08
#switch between local and remote database
# dev for local testing, prod for production
ENV = 'prod'

def connectToDB():
    if ENV == 'dev':
        conn = psycopg2.connect('dbname=postgres port=5432 user=postgres host=localhost', options='-c search_path=Majors')
    else:
        conn = psycopg2.connect('dbname=dckbguanuf8a45 port=5432 user=uxoitcpyfpqfvq host=ec2-44-196-223-128.compute-1.amazonaws.com password=f646a5b031a7b5f570ef097d77f987809613ca53ee77167d1430d246105a0a08', options='-c search_path=Majors')
    return conn.cursor()

#Show all prereq of electives and required classes for this degree
def majorPrereq(degree):
    cur = connectToDB()
    query = "SELECT classID, preReq FROM Requirements WHERE UPPER(gradReq) LIKE UPPER('%%' || %s || '%%')"
    cur.execute(query, (degree,))
    return cur.fetchall()

#Subject Example: CSE, MATH
def allClassesInMajor(major):
    cur = connectToDB()
    query = "SELECT * FROM Classes WHERE UPPER(classID) LIKE UPPER('%%' || %s || '%%')"
    cur.execute(query, (major,))
    return cur.fetchall()

# all attributes for single class
def singleClass(className):
    cur = connectToDB()
    query = "SELECT * FROM Requirements WHERE UPPER(classID) = UPPER(%s)"
    cur.execute(query, (className,))
    return cur.fetchone()

#Requirement for single class
def singleClassRequirement(className):
    cur = connectToDB()
    query = "SELECT preReq FROM Requirements WHERE UPPER(classID) = UPPER(%s)"
    cur.execute(query, (className,))
    return cur.fetchone()
# credit
def singleClassCredit(classID):
    cur = connectToDB()
    query = "SELECT credit FROM Classes WHERE UPPER(classID) = UPPER(%s)"
    cur.execute(query, (classID,))
    return cur.fetchone()

# quarters
def singleClassQuarters(classID):
    cur = connectToDB()
    query = "SELECT quarters FROM Classes WHERE UPPER(classID) = UPPER(%s)"
    cur.execute(query, (classID,))
    return cur.fetchall()

# for frontend search bar
# all classes with attribute classname, subject, credit, quarter
def allClassesByClassName(className, degree):
    cur = connectToDB()
    query = "SELECT className, subject, credit, quarters FROM Classes, Requirements WHERE UPPER(className) LIKE UPPER('%%' || %s || '%%') AND Classes.classID = Requirements.classID AND UPPER(gradReq) LIKE UPPER('%%' || %s || '%%')"
    cur.execute(query, (className, degree))
    return cur.fetchall()

print(requirement('CSE 101'))
#print(allClassesByClassName('MATH',''))