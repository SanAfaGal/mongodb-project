import os

from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure, ConfigurationError
from pymongo.mongo_client import MongoClient


def get_mongo_client():
    # Load config from .env file
    load_dotenv()

    # Validate that mongodb_uri is set
    mongodb_uri = os.getenv('MONGODB_URI')
    if not mongodb_uri:
        raise ValueError("mongodb_uri is not set in the environment variables.")

    try:
        # Connect to MongoDB cluster
        connection = MongoClient(mongodb_uri)

        # Optionally test the connection
        connection.admin.command('ping')
        print("Connected to MongoDB")

        return connection
    except (ConnectionFailure, ConfigurationError) as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise


# Get the MongoDB client
client = get_mongo_client()

# Get reference to a database
db_conn = client.get_database('event_management')
