import os
import sys
import pymongo
import certifi
from dotenv import load_dotenv  # <--- THIS
load_dotenv()  # <--- AND THIS

from src.exception import VehicleException
from src.logger import logging
from src.constants import DATABASE_NAME

ca = certifi.where()

class MongoDBClient:
    client = None

    def __init__(self, database_name: str = DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv('MONGODB_URL')
                if mongo_db_url is None:
                    raise Exception("Environment variable 'MONGODB_URL' is not set.")
                
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
            
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name

            print("MongoDB connection successful.")

        except Exception as e:
            raise VehicleException(e, sys)

if __name__ == "__main__":
    print("Script started")
    mongo = MongoDBClient()
