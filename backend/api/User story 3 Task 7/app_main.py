import imp
from typing import Optional
from fastapi import Body, FastAPI, Response, status,HTTPException
from pydantic import BaseModel
from random import randrange
app = FastAPI()
import ../../src/query.py

#Schema for user input: User must type in input within corresponding schema, or error will be raised
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

class Class_entry(BaseModel):
    class_title: str

class login_entry(BaseModel):
    user_name: str
    password: str

#These are the data for testing api post & update features 
my_posts = [{"title": "app title of post 1", "content": "content of post 1", "id": 1},
{"title": "app title of post 2", "content": "content of post 2", "id": 2}]
# request Get method url: "/"

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
#retrieve data using get: start with the root directory
@app.get("/") 
def root():

    return {"message": "Welcome to Slug Scheduler API!"} # In `return`, it shows the info back to the user

#retrieve all posts
@app.get("/posts")
def get_posts():
    return{"data": my_posts}

#every path parameter passed in as a string. Make sure you manually convert it into type you want
#Use database identifier for the corresponding post to retrieve certain post / entry; if entry does not exist, return HTTP 404 to frontend
@app.get("/posts/{id}")
def get_post(id:int):
    post = find_post(id)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"post_detail":post}

#schema of posts: title str, content str
#load data into certain variable by referencing to a created schema class, which is 'Post' here

#Create a post and add it to the database; return HTTP 201 if succeed
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,10000)
    post_dict['id_num'] = randrange(0,10000)
    my_posts.append(post_dict)
    return{"data": post_dict}


#Delete a post from database, return HTTP 204 on success; if the request post / entry doesn't exist, return HTTP 404
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    #find the index in the array that has required ID
    # my_posts.pop(index)
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
#Update a post from database, return HTTP 200 on success; if the request post / entry doesn't exist, return HTTP 404
@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}

