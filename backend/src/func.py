#####################################################
#Functionalities: (frontend)
#1. Allow users to add classes to our plan template (not stored in database)
#2. Allow users to delete classes (not stored in database)
#3. Search bar - user enter a class string, after submitted, post this string to api endpoint, endpoint will call query function to return a list of classes to the frontend 
#4. Generate an academic plan base on the classes entered (given finished classes, according to the goal, return the remaining ones)
#   1. gather the entered classes from user
#   2. post what user entered to backend
#   3. the verification algo checks if the entered classes are valid according to the prereq; if valid, go next; if not valid, return error
#   4. backend api calls the algorithm to get the remaining classes
#5. Verify whether a certain entered schedule finish a certain goal (given finished class or expected schedule, return if the enter schedule is valid)
#6. Check major requirenments base on the classes entered
#7. GET, POST, DELETE ---- Only methods we need to use in CRUD framework
##################################################### CRUD: post, get, put, delete
import imp
import sys
from typing import Optional
from fastapi import Body, FastAPI, Response, status,HTTPException
import fastapi
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from reqs import requirement
#from test import requirement
app = FastAPI()
ENV = 'prod'

def connectToDB():
    if ENV == 'dev':
        conn = psycopg2.connect('dbname=postgres port=5432 user=postgres host=localhost', options='-c search_path=Majors')
    else:
        conn = psycopg2.connect('dbname=dckbguanuf8a45 port=5432 user=uxoitcpyfpqfvq host=ec2-44-196-223-128.compute-1.amazonaws.com password=f646a5b031a7b5f570ef097d77f987809613ca53ee77167d1430d246105a0a08', options='-c search_path=Majors')
    return conn.cursor()

def allClassesByClassName(className, degree):
    cur = connectToDB()
    query = "SELECT Classes.classID, className, subject, credit, quarters FROM Classes, Requirements WHERE UPPER(className) LIKE UPPER('%%' || %s || '%%') AND Classes.classID = Requirements.classID AND UPPER(gradReq) LIKE UPPER('%%' || %s || '%%')"
    cur.execute(query, (className, degree))
    return cur.fetchall()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
# "title": "<content>"
class searchClass(BaseModel):
    classstr: Optional[str] = ' '
    majorstr: str
class Quarters(BaseModel):
    Fall: list[str]
    Winter: list[str]
    Spring: list[str]
    Summer: list[str]
class enteredclasses(BaseModel):
    First: Quarters
    Second: Quarters
    Third: Quarters
    Fourth: Quarters


@app.get("/")
def root():
    cur = connectToDB()
    return {"message": "Welcome to my api!!!!!!"}
#Notice: this is the path for functionality No.3: search bar
@app.get("/searchclass")
def get_posts(input:searchClass):
    posts = allClassesByClassName(input.classstr, input.majorstr)
    if posts == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"course does not exist")
    return{tuple(posts)}

@app.get("/verification") # verify pre-req quarter-quarter
def verification(entered: enteredclasses):
    #test = Requirement(); test.validate(schedule)
    #print(entered)
    #<Shing's Verification functions>
    req = requirement()
    result = req.validate(entered.dict())
    return(result)

@app.get("/recommendation")
def verification(entered: enteredclasses):
    print(dict(entered))
    #print(entered.classes)
    #<Shing's Course Recommendation functions>
    return(dict(entered))

@app.get("/getFall")
def getFall(entered: Quarters):
    #print(entered.classes)
    return(entered.Fall)




