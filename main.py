# import flast module
from flask import Flask
from routes.user import user_bp
from database import createTables
 
# instance of flask application
app = Flask(__name__)
app.register_blueprint(user_bp, url_prefix = "/api/v1")
try:
    createTables()
except Exception as e:
    print("Error creating tables:", e)
 
# home route that returns below text when root url is accessed
@app.route("/")
def hello_world():
    return {"name" : "jason"}
 
if __name__ == '__main__':  
   app.run(port = 5000)