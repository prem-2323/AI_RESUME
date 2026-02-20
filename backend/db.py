import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

# Create MongoDB client
client = MongoClient(MONGO_URI)

# Access database
db = client[DB_NAME]

print("✅ MongoDB Connected Successfully!")

auth_collection = db["auth"]