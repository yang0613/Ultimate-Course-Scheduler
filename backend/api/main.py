import imp
from typing import Optional
from fastapi import Body, FastAPI, Response, status,HTTPException
import fastapi
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
while True:

    try:
        #conn = psycopg2.connect(host = 'localhost', database = 'fastapi_database', 
        #user = 'postgres', password = '121407', cursor_factory=RealDictCursor)
        conn = psycopg2.connect('dbname=postgres user=postgres host=localhost password = 121407', options='-c search_path=Majors')
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Connecting to database failed!")
        print("Error:", error)
        time.sleep(2)

@app.get("/") # decorator: connect the function to make it run as api; "<path>" => "/" = root path
def root(): #the function time doesn't matter; however it's better to have a descriptor for path operation function
    return {"message": "Welcome to my api!!!!!!"} # In `return`, it shows the info back to the user

# sever/search/CSE/CSE b.s
@app.get("/posts")
def get_posts():
    #cursor.execute("""SELECT * FROM public.posts""")
    #posts = cursor.fetchall()
    posts = allClassesByClassName('CSE', 'Computer Science B.S')
    #print(posts)
    return{tuple(posts)}
#every path parameter passed in as a string. Make sure you manually convert it into type you want
@app.get("/posts/{id}")
def get_post(id:int, response: Response):
    cursor.execute("""SELECT * FROM public.posts WHERE id = %s""", [str(id)])
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"post_detail":post}
# Post request

#schema of posts: title str, content str
#load data into certain variable by referencing to a created schema class, which is 'Post' here

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    #post_dict = post.dict()
    #post_dict['id'] = randrange(0,10000)
    #post_dict['id_num'] = randrange(0,10000)
    #my_posts.append(post_dict)
    #return{"data": post_dict}
    cursor.execute("""INSERT INTO public.posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return{"data": new_post}

#Delete a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""DELETE FROM public.posts WHERE id = %s RETURNING *""", [(str(id))])
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    #return {"message": "post was successfully deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    cursor.execute("""UPDATE public.posts SET title = %s, content = %s, published = %s  WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    #print(post)
    return {"data": updated_post}
    #return {'message': "updated post"}


def allClassesByClassName(className, degree):
    query = "SELECT className, subject, credit, quarters FROM Classes, Requirements WHERE className LIKE '%%' || %s || '%%' AND Classes.classID = Requirements.classID AND gradReq LIKE '%%' || %s || '%%'"
    cursor.execute(query, (className, degree,))
    return cursor.fetchall()