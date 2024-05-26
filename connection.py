import os

from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient

load_dotenv()  # take environment variables from .env.
MONGODB_URI = os.environ['MONGODB_URI']

client = MongoClient(MONGODB_URI)

for db_name in client.list_database_names():
    print(db_name)

client.close()