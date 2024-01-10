from flask import Flask, render_template, request, Response
from lib.framegenerator import generate_frames
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Read environment variable
load_dotenv()
variable_name = 'MONGO_URI'
uri = os.environ[variable_name]

if uri:
    print(f"The value of {variable_name} is: {uri}")
else:
    print(f"{variable_name} is not set.")
    
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Set up database and collection
db = client.xhole
collection = db.data_train

def get_rock_options():
    # Replace this with your actual MongoDB query logic
    # For example, you might use a MongoDB client library
    # to connect to your database and fetch the data
    options = ["Option 1", "Option 2", "Option 3"]
    return options

@app.route('/')
def home():
    apps = ['detector']  # Replace with your actual app names
    return render_template('index.html', title='XHole Detection', apps=apps)

@app.route('/detector')
def detector():
    return render_template('detector.html', title='XHole Detection Main Cam')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/recommend')
def recommend():
    rock_options = get_rock_options()
    return render_template('recommend.html', title='XHole Detection Recommendation', rock_options=rock_options)

# Examples of basic CRUD methods
@app.route("/read")
def read():
    cursor = collection.find()
    for record in cursor:
        name = record["name"]
        print(record)
    return render_template("response.html", res = name)

@app.route("/insert")
def insert():
    name = request.args.get("name")
    address = request.args.get("address")
    myVal = { "name": name, "address": address }
    x = collection.insert_one(myVal)
    return render_template("response.html", res = x)

@app.route("/delete")
def delete():
    name = request.args.get("name")
    myquery = { "name": name }
    collection.delete_one(myquery)
    x = "Record delete"
    return render_template("response.html", res = x)

@app.route("/update")
def update():
    name = request.args.get("name")
    new_address = request.args.get("new_address")
    myquery = { "name": name }
    newvalues = { "$set": { "address": new_address } }
    x = "Record updated"
    collection.update_one(myquery, newvalues)
    return render_template("response.html", res = x)

if __name__ == '__main__':
    app.run(debug=True)
