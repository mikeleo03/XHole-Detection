from flask import Flask, render_template, request, Response
from lib.framegenerator import generate_frames
from lib.algorithm.Rock_Factor import Rock_Factor
from lib.algorithm.KuzRam_Fragmentation import KuzRam_Fragmentation
from lib.algorithm.Rosin_Rammler import Rosin_Rammler
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
stone_data = db.stone

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

@app.route('/result', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        # Access form data
        # 0. Setup rock and explosives
        rock_type = request.form['rock']
        # Ambil 3 constant utamanya
        specific_gravity = 2.9
        hardness = 6.09
        rock_density = 181.0412
        
        explosive_type = request.form['explosives']
        blasting_energy = 0
        blasthole_diameter = 0
        if explosive_type == "TNT":
            blasting_energy = 115
            blasthole_diameter = 0.005
        elif explosive_type == "ANFO":
            blasting_energy = 100
            blasthole_diameter = 0.03
            
        explosives_density = request.form['expdensity']
        detonation_speed = request.form['detspeed']
        
        # 1. Rock Factor
        rock_mass_description = request.form['rmd']
        joint_plane_spacing = request.form['jps']
        joint_plane_orientation = request.form['jpo']
        
        # Calculating the rock factor
        rock_factor_class = Rock_Factor(rock_mass_description, joint_plane_spacing, joint_plane_orientation, specific_gravity, hardness)
        rock_factor = rock_factor_class.run()
        print("Rock factor:", rock_factor)
        
        # 2. Kuz Ram Fragmentation
        high_level = request.form['level']
        ignition_method = request.form['ignition']
        
        rock_deposition = request.form['rockdepo']
        geologic_structure = request.form['geostruc']
        number_of_rows = request.form['rows']  
        
        # Calculating the fragmentation size
        kuzram_class = KuzRam_Fragmentation(explosives_density, detonation_speed, blasting_energy, rock_density, blasthole_diameter, high_level)
        fragmentation_size = kuzram_class.run(rock_factor, rock_deposition, geologic_structure, number_of_rows, ignition_method)
        print("Fragmentation size:", fragmentation_size)
        
        # 3. Rosin-Rammler Calculations
        stdev_drilling_accuracy = request.form['stdevdrill']
        corrected_burden = kuzram_class.get_corrected_burden()
        stiffness = kuzram_class.get_stiffness()
        print("Corrected Burden:", corrected_burden)
        rossin_rammler_class = Rosin_Rammler(stdev_drilling_accuracy, corrected_burden, fragmentation_size, blasthole_diameter, high_level)
        rossin_rammler_class.run(stiffness)

        # Perform any necessary processing, for example, store in MongoDB or run calculations

        # Return a response or redirect to another page
        return render_template('result.html', result="Form submitted successfully!")

    # Handle other HTTP methods or redirect to form page
    return render_template('form_page.html')

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
