from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "digital_personality_twin"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

twins_collection = db["twins"]
conversations_collection = db["conversations"]
