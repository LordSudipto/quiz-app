# Script to add questions into mongoDB
# ---------------------------------------------------------------

# Import libraries
import json
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# ---------------------------------------------------------------

# Connect to mongodb database

# import connection string from another file (.env here)
load_dotenv()
conn_string = os.getenv('mongo_string')     # get mongo_string key's value from .env file

# Make connections to your empty question collections
cluster = MongoClient(conn_string)
db = cluster['Questions']                   # The database in your cluster
collection1 = db['MCQ']                     # The collection in your database
collection2 = db['One Word Answers']        # The collection in your database

# ---------------------------------------------------------------

# Load JSON data
with open('Questions JSON/MCQ questions.json') as f:
    mcq_data = json.load(f)

with open('Questions JSON/One word answers.json') as f:
    owa_data = json.load(f)

# ---------------------------------------------------------------

# Insert MCQs into 'MCQ' mongodb collection.
for i, (key, value) in enumerate(mcq_data.items()):
    value["_id"]=i+1
    collection1.insert_one(value)

# Insert one word answer questions into 'One Word Answers' mongodb collection
for i, (key, value) in enumerate(owa_data.items()):
    value["_id"] = i + 1
    collection2.insert_one(value)

