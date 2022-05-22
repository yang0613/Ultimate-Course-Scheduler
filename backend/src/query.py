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


def allClassByID(classID):
    cur = connectToDB()
    query = "SELECT * FROM Classes, Requirements WHERE Classes.classID = Requirements.classID AND Requirements.classID IN %s" 
    cur.execute(query, (classID,))
    return cur.fetchall()

# for frontend search bar
# all classes with attribute classname, subject, credit, quarter
def allClassesByMajor(major):
    cur = connectToDB()
    query = "SELECT Classes.classID, className, credit, quarters FROM Classes, Requirements WHERE Classes.classID = Requirements.classID AND UPPER(gradReq) LIKE UPPER('%%' || %s || '%%')"
    cur.execute(query, (major,))
    return cur.fetchall()

def database_cache(classID):
    """Returns a dictionary of prerequisites and its avaliable quarters

    Args:
        classID (tuple): A tuple of classes

    Returns:
        dict: A dictionary key delimited by its class ID and whose values
        are dictionaries of each class's associated properties
    """
    database_cache = {}
    cur = connectToDB()
    query = "SELECT Classes.classID, quarters, prereq FROM Classes, Requirements WHERE Classes.classID = Requirements.classID AND Requirements.classID IN %s"
    cur.execute(query, (classID,))
    columns = [col[0] for col in cur.description]
    for row in cur.fetchall():
        course = row[0]
        properties = dict(zip(columns, row))
        properties.pop('classid')
        database_cache[course] = properties
    return database_cache

#print(allClassByID(('CSE 20', 'MATH 19A', 'CSE 12', 'CSE 16', 'CSE 30', 'CSE 13S', 'MATH 21', 'CSE 101', 'MATH 19B', 'CSE 130', 'CSE 103', 'ECE 30', 'CSE 102', 'CSE 120', 'BIOE 20C', 'ENVS 25', 'STAT 7L', 'STAT 7', 'STAT 131', 'ANTH 2', 'CHEM 1A', 'ENVS 130A', 'ENVS 130L', 'ENVS 100', 'ENVS 100L', 'PHYS 5A', 'PHYS 5B', 'AM 114', 'AM 147')))
#print(allClassesByMajor('computer Science B.s.'))