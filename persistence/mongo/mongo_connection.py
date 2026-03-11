'''
Handles creation of MongoDB client and exposes collections
and returns the Mongo collection used for RL experiences.
'''


from pymongo import MongoClient
from pymongo.collection import Collection
from dotenv import load_dotenv
import os


class MongoConnection:

    def __init__(self):
        
        load_dotenv()
        mongo_uri = os.getenv("MONGO_URI")
        mongo_db = os.getenv("MONGO_DB")

        self.client = MongoClient(mongo_uri)
        self.db = self.client[mongo_db]

    def get_simulation_experiences(self) -> Collection:

        return self.db["simulation_experiences"]