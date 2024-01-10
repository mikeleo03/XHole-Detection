import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

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
database_name = client.xhole
collection_name = database_name.stone

# Google Sheets exported CSV file path
csv_file_path = "../data/rock_data.csv"

# Read CSV file into a Pandas DataFrame
df = pd.read_csv(csv_file_path)

# Convert DataFrame to a list of dictionaries (each row becomes a dictionary)
data = df.to_dict(orient='records')

# Insert data into MongoDB collection
collection_name.insert_many(data)

# Close MongoDB connection
client.close()

print("Data inserted successfully.")
