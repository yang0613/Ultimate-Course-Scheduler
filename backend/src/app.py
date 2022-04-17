from flask import Flask

# example code
# Use 'pipenv shell' to start environment
# Use 'flask run' to start server
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"