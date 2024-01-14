from flask import Flask, render_template, request, Response
from lib.framegenerator import generate_frames
from lib.algorithm.Rock_Factor import Rock_Factor
from lib.algorithm.KuzRam_Fragmentation import KuzRam_Fragmentation
from lib.algorithm.Rosin_Rammler import Rosin_Rammler
from lib.algorithm.Cost_Calculation import Cost_Calculation
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import locale
import webbrowser
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)

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

# Repository
def get_rock_options():
    # Retrieve all documents from the collection
    cursor = stone_data.find({})

    # Extract "rock" attribute values from each document
    rock_values = [doc.get("rock") for doc in cursor]
    return rock_values

@app.route('/static/plot.png')
def serve_plot():
    return send_from_directory('static', 'plot.png')

# Register a custom Jinja filter for formatting currency
def format_currency(value):
    locale.setlocale(locale.LC_ALL, 'id_ID')  # Set the locale to Indonesian
    return locale.currency(value, grouping=True)

app.jinja_env.filters['format_currency'] = format_currency

# List of endpoint
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
        # Define the query to retrieve the single document with the specified stone name
        query = {"rock": rock_type}
        # Define the projection to include the three additional attributes
        projection = {"rock": 1, "hardness": 1, "sg": 1, "rho2": 1, "_id": 0}
        # Retrieve the single document based on the query and projection
        result = stone_data.find_one(query, projection)
        # Ambil 3 constant utamanya
        specific_gravity = result['sg']
        hardness = result['hardness']
        rock_density = result['rho2']
        
        explosive_type = request.form['explosives']
        blasting_energy = 0
        blasthole_diameter = 0
        if explosive_type == "TNT":
            blasting_energy = 115
            blasthole_diameter = 0.005
        elif explosive_type == "ANFO":
            blasting_energy = 100
            blasthole_diameter = 0.03
            
        explosives_density = float(request.form['expdensity'])
        detonation_speed = float(request.form['detspeed'])
        
        # 1. Rock Factor
        rock_mass_description = int(request.form['rmd'])
        joint_plane_spacing = int(request.form['jps'])
        joint_plane_orientation = int(request.form['jpo'])
        
        # Calculating the rock factor
        rock_factor_class = Rock_Factor(rock_mass_description, joint_plane_spacing, joint_plane_orientation, specific_gravity, hardness)
        rock_factor = rock_factor_class.run()
        
        # 2. Kuz Ram Fragmentation
        high_level = float(request.form['level'])
        ignition_method = bool(request.form['ignition'])
        
        rock_deposition = int(request.form['rockdepo'])
        geologic_structure = int(request.form['geostruc'])
        number_of_rows = int(request.form['rows'])
        gap_jaw_crusher = int(request.form['jaw'])
        x_kuzram = 0.8 * gap_jaw_crusher
        stdev_drilling_accuracy = float(request.form['stdevdrill'])
        
        # 2. Calculating the fragmentation size
        fragmentation_size = 0       # Initial fragmentation size, m
        while (fragmentation_size < x_kuzram):
            # Kuz-Ram Calculations
            kuzram_class = KuzRam_Fragmentation(explosives_density, detonation_speed, blasting_energy, rock_density, blasthole_diameter, high_level)
            fragmentation_size = kuzram_class.run(rock_factor, rock_deposition, geologic_structure, number_of_rows, ignition_method)
            print("diameter, size:", blasthole_diameter, fragmentation_size)
            if (fragmentation_size < x_kuzram):
                blasthole_diameter += 0.01
            
        print("Expected diameter:", round(blasthole_diameter, 2))
        
        # 3. Validate the diameter quality
        good_diameter = False
        corrected_burden = 0
        while (not good_diameter):
            # Rosin-Rammler Calculations
            corrected_burden = kuzram_class.get_corrected_burden()
            rossin_rammler_class = Rosin_Rammler(stdev_drilling_accuracy, corrected_burden, fragmentation_size, blasthole_diameter, high_level)
            rossin_rammler_class.calculate_rossin(int(2.25 * x_kuzram))
            sieve_size_data, percent_data = rossin_rammler_class.get_rossin_data()
        
            # Doing reggression with all those data and get the sieve_size_data when percent_data = 80
            pos = len(sieve_size_data) - 1
            x_val1 = sieve_size_data[pos]
            y_val1 = percent_data[pos]
            print("Init value, pos:", x_val1, y_val1, pos)
            while (y_val1 > 80):
                y_val1 = percent_data[pos]
                x_val1 = sieve_size_data[pos]
                pos -= 1
            
            # Gather the larger one
            y_val2 = percent_data[pos+2]
            x_val2 = sieve_size_data[pos+2]
            
            # Normalize values
            y_nom2 = y_val2 - 80
            y_nom1 = 80 - y_val1
            y_fix2 = y_nom2 / (y_nom1 + y_nom2)
            y_fix1 = y_nom1 / (y_nom1 + y_nom2)
            
            # Weighting process
            x_val = x_val1 * y_fix1 + x_val2 * y_fix2
            print(x_val1, y_fix1, x_val2, y_fix2)
            print("X Val:", x_val)
            
            # Conditions
            if (x_val >= x_kuzram):
                good_diameter = True
            else:
                blasthole_diameter -= 0.01
            
        print("Final expected diameter:", round(blasthole_diameter, 2))
        rossin_rammler_class.run(int(2.25 * x_kuzram), round(x_val, 3), 80, x_kuzram)
        img_data = rossin_rammler_class.get_image_data()
        space = kuzram_class.get_stiffness()

        # 4. Cost_Calculation
        rock_volume = kuzram_class.get_rock_volume()
        explosive_mass = kuzram_class.get_explosive_mass()
        daily_target = 25000    # bcm/day
        coloumn_charge = rossin_rammler_class.get_coloumn_charge()
        cost_calculation_class = Cost_Calculation(rock_volume, explosive_mass, daily_target, coloumn_charge)
        cost_calculation = cost_calculation_class.run()
        print("Cost calc:", cost_calculation)
        
        # 5. Recommendation section
        recommendation_diameter = 0
        cost_calculation1 = 0
        if (explosive_type == "ANFO" and blasthole_diameter > 0.03):
            recommendation_diameter = blasthole_diameter - 0.01
        elif (explosive_type == "TNT" and blasthole_diameter > 0.005):
            recommendation_diameter = blasthole_diameter - 0.01
            
        if (recommendation_diameter != 0):
            # Kuz-Ram Calculations
            kuzram_class1 = KuzRam_Fragmentation(explosives_density, detonation_speed, blasting_energy, rock_density, recommendation_diameter, high_level)
            fragmentation_size1 = kuzram_class1.run(rock_factor, rock_deposition, geologic_structure, number_of_rows, ignition_method)
            
            # Rosin-Rammler Calculations
            corrected_burden1 = kuzram_class1.get_corrected_burden()
            rossin_rammler_class1 = Rosin_Rammler(stdev_drilling_accuracy, corrected_burden1, fragmentation_size1, recommendation_diameter, high_level)
            rossin_rammler_class1.calculate_rossin(int(2.25 * x_kuzram))
            
            # 4. Cost_Calculation
            rock_volume1 = kuzram_class1.get_rock_volume()
            explosive_mass1 = kuzram_class1.get_explosive_mass()
            coloumn_charge1 = rossin_rammler_class1.get_coloumn_charge()
            cost_calculation_class1 = Cost_Calculation(rock_volume1, explosive_mass1, daily_target, coloumn_charge1)
            cost_calculation1 = cost_calculation_class1.run()
            print("Cost calc:", cost_calculation1)
        
        # Create a dictionary to store all the data
        template_data = {
            'title': 'XHole Detection Recommendation Result',
            'blasthole_diameter': blasthole_diameter,
            'corrected_burden': round(corrected_burden, 4),
            'space': round(space, 4),
            'length': high_level,
            'stemming': round(0.7 * corrected_burden, 4),
            'subdrill': round(0.2 * corrected_burden, 4),
            'amount_of_explosives': round(explosive_mass, 4),
            'powder_factor': round(cost_calculation_class.get_powder_factor(), 4),
            'number_of_blastholes': int(cost_calculation_class.get_holes_number()),
            'avg_fragmentation_size': fragmentation_size,
            'cost_estimation': int(cost_calculation),
            'img_data': img_data,
            'recommended_diameter': recommendation_diameter,
            'recommended_cost': cost_calculation1,
            'joint_plane_orientation': joint_plane_orientation
        }
    
        # Return a response or redirect to another page
        return render_template('result.html', **template_data)

if __name__ == '__main__':
    webbrowser.open_new('http://localhost:5000/')
    app.run()
