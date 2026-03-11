'''
Handles persistence of RL experience documents.
'''


from pymongo.collection import Collection

from datetime import datetime
from typing import List

from persistence.mongo.mongo_connection import MongoConnection
from persistence.mongo.base_collection import SimulationExperienceDocument


class ExperienceRepository:

    def __init__(self, connection: MongoConnection | None = None):

        self.connection = connection or MongoConnection()
        self.collection: Collection = self.connection.get_simulation_experiences()

    def insert_game_experience(self, document: SimulationExperienceDocument) -> str:

        # Inserts a full game experience document.

        document["created_at"] = datetime.utcnow()

        result = self.collection.insert_one(document)

        return str(result.inserted_id)

    def insert_many(self, documents: List[SimulationExperienceDocument]):


        # Bulk insert for faster dataset writing.


        for doc in documents:
            doc["created_at"] = datetime.utcnow()

        self.collection.insert_many(documents)

    def get_by_simulation(self, simulation_run_id: int):


        # Fetch all experience documents for a simulation run.


        return self.collection.find({
            "simulation_run_id": simulation_run_id
        })

    def get_by_game(self, simulation_run_id: int, game_id: int):


        # Fetch a specific game trajectory.


        return self.collection.find_one({
            "simulation_run_id": simulation_run_id,
            "game_id": game_id
        })