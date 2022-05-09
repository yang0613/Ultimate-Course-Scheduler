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
    rating: Optional[int] = None
while True:

    try:
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi_database', 
        user = 'postgres', password = '121407', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Connecting to database failed!")
        print("Error:", error)
        time.sleep(2)

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
{"title": "title of post 2", "content": "content of post 2", "id": 2}]
# request Get method url: "/"

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
@app.get("/") # decorator: connect the function to make it run as api; "<path>" => "/" = root path
def root(): #the function time doesn't matter; however it's better to have a descriptor for path operation function
    return {"message": "Welcome to my api!!!!!!"} # In `return`, it shows the info back to the user


@app.get("/posts")
def get_posts():
    #return{"data": "This is your posts"}
    return{"data": my_posts}
#every path parameter passed in as a string. Make sure you manually convert it into type you want
@app.get("/posts/{id}")
def get_post(id:int, response: Response):
    #post = find_post(int(id))
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message":f"post with id: {id} was not found"}
    return {"post_detail":post}
# Post request
'''
@app.post("/post")
def create_posts():
    return {"message" : "Your post created successfully"}
'''
'''
@app.post("/post")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return { "Your post created successfully": f"title: {payload['title']}, content: {payload['content']}"}
'''
'''
@app.post("/createposts")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return{"new_post" : f"title {payload['title']} content:{payload['content']}"}
'''

#schema of posts: title str, content str
#load data into certain variable by referencing to a created schema class, which is 'Post' here

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    #print(post)
    #print(post.dict())
    post_dict = post.dict()
    post_dict['id'] = randrange(0,10000)
    post_dict['id_num'] = randrange(0,10000)
    my_posts.append(post_dict)
    return{"data": post_dict}

    #return{"message": "successfully created the post"}

#Delete a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    #find the index in the array that has required ID
    # my_posts.pop(index)
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    my_posts.pop(index)
    #return {"message": "post was successfully deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    #print(post)
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
    #return {'message': "updated post"}

