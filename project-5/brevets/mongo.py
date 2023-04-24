

from pymongo import MongoClient
import os
# Set up MongoDB connection
client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)

# Use database "todo"
db = client.brevet

# Use collection "lists" in the databse
collection = db.lists


def get_data():
    lists = collection.find().sort("_id", -1).limit(1)

    for info in lists: 
        return info["distance"], info["other"]

def insert_new(distance, other): 
    output = collection.insert_one({
        "distance":distance,
        "other": other
    })
    _id = output.inserted_id
    return str(_id)
